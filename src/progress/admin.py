from django.contrib import admin
from .models import Progress


###### Admin should not be able to change the users Progress or details!


class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_updated', 'current_bmi', 'target_bmi')
    search_fields = ('user__username',)

admin.site.register(Progress, ProgressAdmin)


