from django.contrib import admin

from .models import Meal

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('diet', 'meal_date', 'recipe')

admin.site.register(Meal, RecipeAdmin)
