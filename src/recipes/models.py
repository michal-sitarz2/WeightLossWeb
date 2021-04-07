from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    # The meal name
    name = models.CharField(max_length=100, blank=False)

    # ID given by spoonacular
    recipe_id = models.IntegerField(validators=[MinValueValidator(0)], unique=True, blank=False)

    # What kind of meal this is. (Breakfast, Lunch, Dinner)
    meal_type = models.CharField(max_length=100, blank=False)

    # Image URL
    image_link = models.CharField(max_length=150, blank=True, null=True)

    # Ingredients
    ingredients = models.TextField(null=True)

    # Servings
    servings = models.IntegerField(validators=[MinValueValidator(0)], default=1)

    # Nutrition info
    #energy = models.FloatField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    carbs = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    fats = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    calories = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    saturated_fats = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    sugars = models.FloatField(validators=[MinValueValidator(0)], blank=False)


    ### Some simple tags to allow us to sort the meals for user preference.
    ### We might need more or we might want to reduce the number of tags.

    # vegetarian = models.BooleanField(default=False)
    # vegan = models.BooleanField(default=False)
    # gluten_free = models.BooleanField(default=False)
    # halaal = models.BooleanField(default=False)
    # shellfish_free = models.BooleanField(default=False)
    # lactose_free = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    #
    # # Lets us check if the meal meets the dietary requirements
    # def check_requirements(restrictions_list):
    #     '''
    #     Pass the requirements as a list of strings where each string
    #     is a requirement that must be true. eg ['vegan', 'shellfish_free']
    #     '''
    #
    #     requirements = {
    #         'vegetarian':self.vegetarian,
    #         'vegan':self.vegan,
    #         'gluten_free':self.gluten_free,
    #         'halaal':self.halaal,
    #         'shellfish_free':self.shellfish_free,
    #         'lactose_free':self.lactose_free
    #         }
    #
    #     for restriction in restrictions_list:
    #         # If any requirement is false, we return false as all must be true
    #         if not requirements[restriction]:
    #             return False
    #     return True
