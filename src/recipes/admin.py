from django.contrib import admin

from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'servings', 'protein', 'carbs', 'fats')
    search_fields = ('title',)

admin.site.register(Recipe, RecipeAdmin)