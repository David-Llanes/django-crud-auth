from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', ) # lleva la coma porque es una tupla de un elemento.

# Register your models here.
admin.site.register(Task, TaskAdmin)