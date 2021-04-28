from django.test import TestCase
from .scripts.bmi_calculate import calculate_BMI
from django.test import Client
import time


class BMIHomePage(TestCase):
    def setUp(self):
        self.client = Client()


    # TODO
    #   this will change pages
    def test_BMI_inputs(self):
        # Calling the bmi calculator without any parameters
        response = self.client.get('/bmi/', follow=True)
        # Confirming that the bmi is set to -2 (indicating that a value was not set yet)
        self.assertEqual(response.context['bmi'], -2)

        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': 100, 'height_metric': 1.85}, follow=True)
        # Confirming that the bmi was calculated correctly
        self.assertEqual(response.context['bmi'], 29.22)

        # Calling the bmi page with get and invalid parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': -1, 'height_metric': 1.85}, follow=True)
        # Confirm that the error flag was set due to invalid input
        self.assertEqual(response.context['bmi'], -1)

    def test_BMI_messages(self):
        # Calling the bmi calculator without any parameters
        response = self.client.get('/bmi/', follow=True)
        # Checking that a message is given to a user to enter inputs to get their BMI (hence flag is set to -2)
        self.assertTrue(b"Please enter your details to calculate your BMI." in response.content)

        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': 100, 'height_metric': 1.85}, follow=True)
        # Checking that a message is given to a user to enter inputs to get their BMI
        self.assertTrue(b"<strong>BMI</strong>: 29.22" in response.content)

        # Calling the bmi page with get and invalid parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': -1, 'height_metric': 1.85}, follow=True)
        # Checking that a message is given to a user that there was an error (hence flag is set to -1)
        self.assertTrue(b"Please enter correct inputs. This includes using positive numbers and checking whether "
                        b"kilograms and meters were used." in response.content)


class BMIInputsTestCase(TestCase):
    def test_calculate_BMI_valid_1(self):
        height = 1.65
        weight = 85
        bmi_calculated = round((weight / height**2), 2)
        self.assertEqual(calculate_BMI(weight,height), bmi_calculated)

    def test_calculate_BMI_valid_2(self):
        height = 1.65
        weight = 85
        self.assertEqual(calculate_BMI(weight,height), 31.22)

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

    # Testing if error is indicated when the inputs are not numbers
    def test_calculate_BMI_negative_weight(self):
        height = "Hello World"
        weight = "Hello World"
        self.assertEqual(calculate_BMI(weight, height), -1)

    # Testing if error is indicated when height is set to zero (as it cannot be zero)
    def test_BMI_zero_height(self):
        height = 0
        weight = 100
        self.assertEqual(calculate_BMI(weight, height), -1)

    # Testing if error is indicated when weight is set to zero (as it cannot be zero)
    def test_BMI_zero_height(self):
        height = 1.85
        weight = 0
        self.assertEqual(calculate_BMI(weight, height), -1)

    # Testing if error is indicated if height is out of range (max set to 3m)
    # Checking mainly because people can put centimeters by accident instead of meters
    def test_calcultate_BMI_invalid_height(self):
        height = 180
        weight = 85
        self.assertEqual(calculate_BMI(weight, height), -1)

class BMIRangeAndTiming(TestCase):
    def setUp(self):
        self.client = Client()

    # Testing that the range is given to the user after they calculate their BMI
    def test_ranges_provided(self):
        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', follow=True)

        # Expecting an error as there should be no range set if BMI wasn't calculated
        with self.assertRaises(KeyError) as context:
            print(response.context['range'])

        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': 100, 'height_metric': 1.85}, follow=True)
        # The range in which the client is expected to be with height 100 and weight 1.85 is overweight
        self.assertEqual(response.context['range'], "Overweight")


        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': 60, 'height_metric': 1.85}, follow=True)
        # The range in which the client is expected to be with height 60 and weight 1.85 is underweight
        self.assertEqual(response.context['range'], "Underweight")

    # Testing how long it takes for the client to get their BMI score
    def test_BMI_retrieval_time(self):
        # Starting the timer
        start = time.time()

        # Calling the bmi page with get and required parameters (indicating inputs)
        response = self.client.get('/bmi/', {
            'weight_metric': 100, 'height_metric': 1.85}, follow=True)

        # Ending the timer
        end = time.time()

        # Verifying that the value is correct
        self.assertEqual(response.context['bmi'], 29.22)

        # Getting the time difference between start and finish
        delta_time = end-start

        # Verifying that it took less than 3 seconds
        self.assertTrue(delta_time < 3)


