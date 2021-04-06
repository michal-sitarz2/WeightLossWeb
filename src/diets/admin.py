from django.contrib import admin
from .models import Diet


class DietAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date')
    search_fields = ('user__username', 'start_date')

admin.site.register(Diet,DietAdmin)
