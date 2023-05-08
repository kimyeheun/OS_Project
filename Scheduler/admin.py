from django.contrib import admin
#
# # Register your models here.
from Scheduler.models import Process, Simulator, PCore, ECore, GanttChart


class ProcessAdmin(admin.TabularInline):
    model = Process


admin.site.register(Process)
admin.site.register(Simulator)
admin.site.register(PCore)
admin.site.register(ECore)
admin.site.register(GanttChart)

