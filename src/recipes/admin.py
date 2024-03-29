from django.contrib import admin

from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Recipe, RecipeAdmin)
