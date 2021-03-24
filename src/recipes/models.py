from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    title = models.CharField(max_length=100, blank=False)
    energy = models.FloatField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)])
    carbs = models.FloatField(validators=[MinValueValidator(0)])
    fats = models.FloatField(validators=[MinValueValidator(0)])
    servings = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.title