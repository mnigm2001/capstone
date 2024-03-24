from django.contrib import admin
from .import models

class pillAdmin(admin.ModelAdmin):
    list_display = ['name', 'shape']


# Register your models here.
admin.site.register(models.Pill, pillAdmin)