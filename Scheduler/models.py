from django.db import models


class Process(models.Model):
    Simulator = models.ForeignKey('Simulator', on_delete=models.CASCADE, default=1)
    Process = models.CharField(max_length=250, default=1)
    AT = models.CharField(max_length=250, default=0)
    BT = models.CharField(max_length=250, default=0)
    WT = models.CharField(max_length=250, default=0)
    TT = models.CharField(max_length=250, default=0)
    NTT = models.CharField(max_length=250, default=0)

    def __str__(self):
        return str(self.Simulator.name) + '-' + self.Process


class Simulator(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(default=1)
    Algorithm = models.CharField(max_length=250, null=True, default='MyAlgorithm')
    quantum = models.IntegerField(null=True, default=0)

    def __str__(self):
        return 'Simulation' + str(self.name)

    def __repr__(self):
        return 'Simulation' + str(self.name)


class PCore(models.Model):
    Simulator = models.ForeignKey('Simulator', on_delete=models.CASCADE, default=1)
    name = models.IntegerField(default=1)
    powerConsumption = models.CharField(max_length=250)
    powerEfficiency = models.CharField(max_length=250)

    def __str__(self):
        return str(self.Simulator.name) + '-PCore' + str(self.name)


class ECore(models.Model):
    Simulator = models.ForeignKey('Simulator', on_delete=models.CASCADE, default=1)
    name = models.IntegerField(default=1)
    powerConsumption = models.CharField(max_length=250)
    powerEfficiency = models.CharField(max_length=250)

    def __str__(self):
        return str(self.Simulator.name) + '-ECore' + str(self.name)


class GanttChart(models.Model):
    Simulator = models.ForeignKey('Simulator', on_delete=models.CASCADE, default=1)
    timeTable = models.CharField(max_length=1000)
    finishTime = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Simulator.name) + '-GanttChart'
