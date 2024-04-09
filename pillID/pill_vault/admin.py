
from django.contrib import admin
from .import models

class pillAdmin(admin.ModelAdmin):
    list_display = ['name', 'shape']
    search_fields = ['name', 'imprint']


# Register your models here.
admin.site.register(models.Pill, pillAdmin)
admin.site.register(models.PillReminder)
admin.site.register(models.PillIntake)
admin.site.register(models.PillScanHistory)
