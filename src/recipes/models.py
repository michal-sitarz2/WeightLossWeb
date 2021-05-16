from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    # The meal name
    name = models.CharField(max_length=100, blank=False, unique=False)

    # ID given by Spoonacular
    recipe_id = models.IntegerField(validators=[MinValueValidator(0)], unique=False, blank=False)

    # What kind of meal this is. (Breakfast, Lunch, Snack, Dinner)
    meal_type = models.CharField(max_length=100, blank=False)

    # Image URL
    image_link = models.CharField(max_length=150, blank=True, null=True)

    # Ingredients
    ingredients = models.TextField(null=True)

    # Servings
    servings = models.IntegerField(validators=[MinValueValidator(0)], default=1)

    # Summary
    summary = models.TextField(blank=True)

    # Source link
    source_link = models.CharField(max_length=200, blank=True)

    # Nutrition info
    #energy = models.FloatField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    carbs = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    fats = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    calories = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    saturated_fats = models.FloatField(validators=[MinValueValidator(0)], blank=False)
    sugars = models.FloatField(validators=[MinValueValidator(0)], blank=False)


    def __str__(self):
        return "{} ({})".format(self.name, self.meal_type)
