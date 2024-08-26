from django.contrib import admin
from .models import Task

#  como el campo created no aparece en task, lo puedo agregar de esta forma, seria un campo de solo lectura


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )


    # Register your models here.
admin.site.register(Task, TaskAdmin)
