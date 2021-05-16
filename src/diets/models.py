from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Account

class Diet(models.Model):
    # One-to-one relationship with the Users Account
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

    # The date that the diet began. This should NOT be updated later on.
    start_date = models.DateTimeField(auto_now_add=True)

    # Save the below fields as string values, which can be passed on as a query string to the API
    # The validation of whether they can be used can be performed in the form (e.g. it has to be comma separated list)
    exclude_cuisines = models.CharField(max_length=100, blank=True)
    exclude_ingredients = models.CharField(max_length=100, blank=True)
    diets = models.CharField(max_length=100, blank=True)
    intolerances = models.CharField(max_length=100, blank=True)

    daily_calories = models.FloatField(blank=False, validators=[MinValueValidator(0)])

    
    def __str__(self):
        return self.user.username
