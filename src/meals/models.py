from django.db import models
from diets.models import Diet
from recipes.models import Recipe

class Meal(models.Model):
    # The date that the meal is expected to be eaten on.
    meal_date = models.DateTimeField(blank=False)
    
    # Many to one relationship with the Diet and Recipe tables
    # The diet that the meal is part of.
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)

    # The recipe that the meal is made up of.
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return "Recipe: {}\nDiet: {}\nMeal Date: {}".format(self.recipe, self.diet, self.meal_date.date())

