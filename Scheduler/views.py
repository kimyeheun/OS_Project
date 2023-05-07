from django.http import QueryDict, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from .forms import ProcessFormSet, SimulatorForm
from .logic import doAlgorithm
from .models import Process, Simulator, PCore, ECore


def index(request):
    return render(request, 'index.html')


def showInfo(request):
    return render(request, 'showLog.html')


class Index(TemplateView):
    template_name = "index.html"

    def get(self, *args, **kwargs):
        process_formset = ProcessFormSet(queryset=Process.objects.none())
        simulator_form = SimulatorForm()
        simulatorLog = Simulator.objects.all()
        return self.render_to_response({'process_formset': process_formset,
                                        'simulator_form': simulator_form,
                                        'simulatorLog': simulatorLog.values()})

    def post(self, *args, **kwargs):
        requestPost = QueryDict(self.request.POST.get('QueryDict'))

        # 값 파씽 해오는 부분
        algorithm = requestPost.get('Algorithm')
        quantum = requestPost.get('quantum')

        if quantum == '':
            quantum = 0

        # 시뮬레이션 넣기
        name = int(Simulator.objects.count()) + 1
        new_simulator = Simulator(name=name)
        new_simulator.save()
        saved_simulator = Simulator.objects.last()
        saved_simulator.quantum = quantum
        saved_simulator.Algorithm = algorithm
        saved_simulator.save()

        # 값 파씽
        processCnt = int(requestPost.get('processCnt'))
        PCoreCnt = int(requestPost.get('PCoreCnt'))
        ECoreCnt = int(requestPost.get('ECoreCnt'))

        # 코어 저장 하기
        saved_simulator = Simulator.objects.last()
        for i in range(PCoreCnt):
            new_pcore = PCore(Simulator=saved_simulator, name=i + 1, powerConsumption=0.0, powerEfficiency=0.0)
            new_pcore.save()
        for i in range(ECoreCnt):
            new_ecore = ECore(Simulator=saved_simulator, name=i + 1, powerConsumption=0.0, powerEfficiency=0.0)
            new_ecore.save()

        # 값 파씽 하기
        process_formset = ProcessFormSet(data=requestPost)
        cnt = 0

        # 프로세서 저장 하기
        processes = process_formset.save(commit=False)
        for process in processes:
            cnt += 1
            process.Simulator = saved_simulator
            process.Process = 'Process' + str(cnt)
            process.save()

        # 시물레이터 pk를 가진 모든 프로세서들을 불러옴
        originalInfo = []
        processAll = Process.objects.filter(Simulator__name=saved_simulator.name)
        for processOne in processAll:
            originalInfo.append(int(processOne.AT))
            originalInfo.append(int(processOne.BT))

        # 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수
        newInfo = doAlgorithm(int(processCnt), int(quantum), originalInfo, int(PCoreCnt), int(ECoreCnt), algorithm)
        idx = 0
        for processOne in processAll:
            i = 0
            while i < 3:
                processOne.WT = int(newInfo[idx])
                processOne.TT = int(newInfo[idx+1])
                processOne.NTT = int(newInfo[idx+2])
                i += 1
                processOne.save()
            idx += i

        url = '/' + str(saved_simulator.name) + '/'
        return HttpResponse(url)


class ShowLog(DetailView):
    template_name = 'showLog.html'

    def get(self, *args, **kwargs):
        processAll = Process.objects.filter(Simulator__name=self.kwargs.get('pk'))
        PCoreAll = PCore.objects.filter(Simulator__name=self.kwargs.get('pk'))
        ECoreAll = ECore.objects.filter(Simulator__name=self.kwargs.get('pk'))
        SimulatorInfo = Simulator.objects.get(name=self.kwargs.get('pk'))
        simulatorLog = Simulator.objects.all()
        return render(self.request, 'showLog.html', {'processAll': processAll,
                                                     'PCoreAll': PCoreAll,
                                                     'ECoreAll': ECoreAll,
                                                     'SimulatorInfo': SimulatorInfo,
                                                     'simulatorLog': simulatorLog.values()})
