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

    daily_calories = models.FloatField(blank=False, default=1200, validators=[MinValueValidator(0)])


    # '''
    # The total nutrition since the start of the diet. This should let us
    # have a 'memory' of previous week's nutrition and let us balance out
    # any disproportionate diets. This is a first implementation and
    # something I want to review a bit more since there isn't loads of
    # research or planning behind how this works.
    #
    # -Oliver
    # '''
    #
    # total_energy = models.FloatField(validators=[MinValueValidator(0)])
    # total_protein = models.FloatField(validators=[MinValueValidator(0)])
    # total_carbs = models.FloatField(validators=[MinValueValidator(0)])
    # total_fats = models.FloatField(validators=[MinValueValidator(0)])

    # Some simple tags to allow us to sort the meals for user preference.
    # We might need more or we might want to reduce the number of tags.

    ### vegetarian = models.BooleanField(default=False)
    ### vegan = models.BooleanField(default=False)
    ### gluten_free = models.BooleanField(default=False)
    ### halaal = models.BooleanField(default=False)
    ### shellfish_free = models.BooleanField(default=False)
    ### lactose_free = models.BooleanField(default=False)


    
    def __str__(self):
        return self.user.username + '\nDiet Start Date: ' + str(self.start_date)
