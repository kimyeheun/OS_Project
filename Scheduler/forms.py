from django import forms
from django.forms import modelformset_factory

from .models import Process, Simulator, PCore, ECore


# 프로세스 AT,BT 받는 폼
class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ["AT", "BT"]


ProcessFormSet = modelformset_factory(
    Process,
    fields=("AT", "BT"),
    extra=1  # extra 는 화면에 처음 표시할 양식의 수
)


class SimulatorForm(forms.ModelForm):
    class Meta:
        model = Simulator
        fields = ['name', 'Algorithm', 'quantum']
        widgets = {
            'Algorithm': forms.Select(choices=[('MyAlgorithm', 'MyAlgorithm'),
                                               ('FCFS', 'FCFS (First Come First Service)'),
                                               ('RR', 'RR (Round Robin)'),
                                               ('SPN', 'SPN (Shortest Process Next)'),
                                               ('HRRN', 'HRRN (Highest Response Ratio Next)'),
                                               ('SRTN', 'SRTN (Shortest Remaining Time Next)')])
        }


class SimulatorLogForm(forms.ModelForm):
    class Meta:
        model = Simulator
        fields = ['name']


class PCoreForm(forms.ModelForm):
    class Meta:
        model = PCore
        fields = ['powerConsumption', 'powerEfficiency']


class ECoreForm(forms.ModelForm):
    class Meta:
        model = ECore
        fields = ['powerConsumption', 'powerEfficiency']
