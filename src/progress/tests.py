from django.test import TestCase
import unittest
from .models import Progress
from account.models import Account
from pages.scripts.bmi_calculate import calculate_BMI

class ProgressTestCase(unittest.TestCase):
    def setUp(self):
        user = Account.objects.create(username='admin', password='admin123', email='admin123@gmail.com')

        self.progress = Progress(starting_height=1.85,
                                 starting_weight=100,
                                 user=user,
                                 target_bmi=20)


    def test_progress_current_creation(self):
        self.progress.initial_current_set()
        self.assertEqual(self.progress.starting_weight, self.progress.current_weight)
        self.assertEqual(self.progress.starting_height, self.progress.current_height)

        self.assertEqual(self.progress.current_bmi,
                         calculate_BMI(self.progress.current_weight, self.progress.current_height))

