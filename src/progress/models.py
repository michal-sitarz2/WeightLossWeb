from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from WebsiteHome.src.models import Account
from account.models import Account

class Progress(models.Model):
    profile = models.ForeignKey(Account, blank=False, on_delete=models.CASCADE)

    current_height = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(3)], blank=False)
    current_weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(400)], blank=False)
    current_bmi = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(400)], blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.username