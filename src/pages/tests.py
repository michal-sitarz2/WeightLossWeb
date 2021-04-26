from django.test import TestCase
from .scripts.bmi_calculate import calculate_BMI

class BMITestCase(TestCase):
    def test_calculate_BMI_valid_1(self):
        height = 1.65
        weight = 85
        bmi_calculated = round((weight / height**2), 2)
        self.assertEqual(calculate_BMI(weight,height), bmi_calculated)

    # Testing if error is indicated when height is negative
    def test_calculate_BMI_negative_height(self):
        height = -10
        weight = 85
        self.assertEqual(calculate_BMI(weight,height), -1)

    # Testing if error is indicated when weight is negative
    def test_calculate_BMI_negative_weight(self):
        height = 1.5
        weight = -10
        self.assertEqual(calculate_BMI(weight,height), -1)

    # Testing if error is indicated if height is out of range (max set to 3m)
    # Checking mainly because people can put centimeters by accident instead of meters
    def test_calcultate_BMI_invalid_height(self):
        height = 150
        weight = 85
        self.assertEqual(calculate_BMI(weight, height), -1)

