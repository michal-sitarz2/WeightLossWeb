from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from django.utils import timezone
from account.models import Account
from pages.scripts.bmi_calculate import calculate_BMI

class Progress(models.Model):
    # One-to-one relationship with the Users Account
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)

    # Weight in Kilograms
    starting_weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(400)], blank=False)
    # Height in meters
    starting_height = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(3)], blank=False)
    # BMI for the user
    current_bmi = models.FloatField(validators=[MinValueValidator(10), MaxValueValidator(50)], blank=True)
    # Goal for the user to reach
    target_bmi = models.FloatField(validators=[MinValueValidator(10), MaxValueValidator(50)], blank=False)
    # Current Height
    current_height = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(3)], default=0)
    # Current Weight
    current_weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(400)], default=0)
    # Details last updated
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)

    # Streak of completing the recipes
    streak = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    # Method to set the current weight and height to intial weight and height
    def initial_current_set(self):
        if not self.starting_height:
            raise ValueError
        if not self.starting_weight:
            raise ValueError

        self.current_weight = self.starting_weight
        self.current_height = self.starting_height
        self.update_bmi()

    # Method to update the bmi for the user based on the current weight and height
    def update_bmi(self):
        self.current_bmi = calculate_BMI(self.current_weight, self.current_height)

    # Method to update the current weight and height, based on user input
    def update_current_set(self, height, weight):
        self.current_weight = weight
        self.current_height = height

        self.update_bmi()
        self.last_updated = timezone.now()

    def __str__(self):
        return self.user.username + "\nStarting Weight: " + str(self.starting_weight) + "\nCurrent Weight: " \
               + str(self.current_weight) + "\nLast Updated: " + str(self.last_updated.date()) + " " + str(self.last_updated.hour)\
               + ":" + str(self.last_updated.minute)
