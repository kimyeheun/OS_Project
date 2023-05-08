from django.http import QueryDict, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
import json

from .forms import ProcessFormSet, SimulatorForm
from .logic import doAlgorithm
from .models import Process, Simulator, PCore, ECore, GanttChart


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
        processCnt = int(requestPost.get('processCnt'))
        PCoreCnt = int(requestPost.get('PCoreCnt'))
        ECoreCnt = int(requestPost.get('ECoreCnt'))
        process_formset = ProcessFormSet(data=requestPost)
        if quantum == '':
            quantum = int(0)
        else:
            quantum = int(quantum)

        # 에러 처리 - 유효한 값이 아니면 경고 후 redirect
        if PCoreCnt == 0 and ECoreCnt == 0:
            return HttpResponseBadRequest("코어가 없습니다.")
        if algorithm == "none":
            return HttpResponseBadRequest("알고리즘이 선택 되어있지 않습니다.")
        if (algorithm == "RR" or algorithm == "MyAlgorithm") and quantum == 0:
            return HttpResponseBadRequest("Time Quantum이 입력 되어있지 않습니다.")

        # 시뮬레이션 넣기
        name = int(Simulator.objects.count()) + 1
        new_simulator = Simulator(name=name, quantum=quantum, Algorithm=algorithm)
        new_simulator.save()
        # saved_simulator = Simulator.objects.last()

        # 코어 저장
        saved_simulator = Simulator.objects.last()
        for i in range(PCoreCnt):
            new_pcore = PCore(Simulator=saved_simulator, name=i + 1, powerConsumption=0.0, powerEfficiency=0.0)
            new_pcore.save()
        for i in range(ECoreCnt):
            new_ecore = ECore(Simulator=saved_simulator, name=i + 1, powerConsumption=0.0, powerEfficiency=0.0)
            new_ecore.save()

        # 프로세서 저장
        cnt = 0
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

        # 알고리즘 적용 단계
        # 프로세스 개수, 타임 퀀텀, [AT, BT], p코어 개수, e코어 개수
        resultInfo = doAlgorithm(int(processCnt), int(quantum), originalInfo, int(PCoreCnt), int(ECoreCnt), algorithm)

        # todo : 간트 차트로 값 넘기기
        try:
            forGantt = resultInfo.get('transport')
            maxFT = resultInfo.get('maxFT')
        except AttributeError:
            return HttpResponseBadRequest()

        # 프로세스 WT, TT, NTT 넣고 저장
        idx = 0
        for processOne in processAll:
            processOne.WT = int(resultInfo.get('newInfo')[idx])
            processOne.TT = int(resultInfo.get('newInfo')[idx + 1])
            processOne.NTT = int(resultInfo.get('newInfo')[idx + 2])
            processOne.save()
            idx += 3

        # 간트 차트에 필요한 정보 저장
        print(forGantt)
        print(maxFT)
        timeTable = json.dumps(forGantt)
        FT = int(maxFT)
        print("----------")
        print(timeTable)
        print(FT)
        print("----------")
        new_ganttChart = GanttChart(Simulator=saved_simulator, timeTable=timeTable, finishTime=FT)
        new_ganttChart.save()

        url = '/' + str(saved_simulator.name) + '/'
        return HttpResponse(url)


class ShowLog(DetailView):
    template_name = 'showLog.html'

    def get(self, *args, **kwargs):
        processAll = Process.objects.filter(Simulator__name=self.kwargs.get('pk'))
        PCoreAll = PCore.objects.filter(Simulator__name=self.kwargs.get('pk'))
        ECoreAll = ECore.objects.filter(Simulator__name=self.kwargs.get('pk'))
        SimulatorInfo = Simulator.objects.get(name=self.kwargs.get('pk'))
        GanttChartInfo = GanttChart.objects.filter(Simulator__name=self.kwargs.get('pk'))
        # print(GanttChartInfo)
        # print(GanttChartInfo.values())
        # # print(GanttChartInfo.values().get('QuerySet'))
        # print("info")
        # print(GanttChartInfo.values_list('timeTable', flat=True))
        simulatorLog = Simulator.objects.all()
        return render(self.request, 'showLog.html', {'processAll': processAll,
                                                     'PCoreAll': PCoreAll,
                                                     'ECoreAll': ECoreAll,
                                                     'SimulatorInfo': SimulatorInfo,
                                                     'GanttChartInfo': GanttChartInfo.values(),
                                                     'simulatorLog': simulatorLog.values()})
