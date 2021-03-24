from django.contrib import admin
from .models import Progress

class ProgressAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date', 'current_bmi')
    search_fields = ('profile__username',)

admin.site.register(Progress, ProgressAdmin)