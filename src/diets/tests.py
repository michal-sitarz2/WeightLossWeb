from django.test import TestCase
from django.db.utils import IntegrityError
from django.test import Client
from django.contrib.auth import logout
from django.test import RequestFactory
from account.models import Account
from progress.models import Progress
from .models import Diet
from .forms import PreferencesForm
import unittest
import datetime

# Class to test diet model
class DietModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.account = Account(username='username1', password='password1', email='user1@gmail.com')
        self.account.save()

    def tearDown(self) -> None:
        self.account.delete()

    # Diet is required to have a user to be saved
    def test_no_user(self):
        # Making a diet without the user
        diet = Diet(daily_calories=2200)

        # Expecting Integrity Error as diet cannot be saved without user
        with self.assertRaises(IntegrityError) as context:
            diet.save()

    # Diet is required to have a daily calories intake
    def test_no_calories(self):
        # Making a diet without calories
        diet = Diet(user=self.account)

        # Expecting an Exception to be thrown as diet cannot be saved without calories
        with self.assertRaises(IntegrityError) as context:
            diet.save()

    # Saving valid meal for a user
    def test_saving_valid_required_and_optional(self):
        # Making a diet with all the required fields
        diet = Diet(user=self.account, daily_calories=2200)
        # Saving the diet
        diet.save()

        # Checking if user has the diet
        self.assertEqual(self.account.diet.daily_calories, 2200)

        # Checking whether start date is set to today's date
        self.assertEqual(self.account.diet.start_date.day, datetime.datetime.today().day)

        # Adding optional fields
        diet.exclude_cuisines = "american, jamaican"
        diet.exclude_ingredients = "eggs"
        diet.intolerances = "dairy"
        diet.diets = "gluten free"
        # Saving diet with optional fields
        diet.save()

        self.assertEqual(self.account.diet.exclude_ingredients, "eggs")
        self.assertEqual(self.account.diet.exclude_cuisines, "american, jamaican")
        self.assertEqual(self.account.diet.intolerances, "dairy")
        self.assertEqual(self.account.diet.diets, "gluten free")

        diet.delete()

    # Checking whether user's diet is deleted with the user
    def test_delete_meal_with_user(self):
        account = Account(username='username3', password='password3', email='user3@gmail.com')
        account.save()

        diet = Diet(user=account, daily_calories=2200)
        diet.save()

        self.assertEqual(account.diet.pk, diet.pk)

        account.delete()

        self.assertEqual(len(Diet.objects.filter(user=account)), 0)

    # Checking that the user cannot have more than one diet
    def test_duplicate_diets_for_user(self):
        # Making a diet for a user with daily calories
        diet = Diet(user=self.account, daily_calories=2200)
        # Saving a diet for the user
        diet.save()

        # Making a second diet for a user with daily calories
        diet2 = Diet(user=self.account, daily_calories=2500)

        # Expecting IntegrityError when saving the diet
        # as there already exists a duplicate diet for the user in the database
        with self.assertRaises(IntegrityError) as context:
            diet2.save()

# Class to test diet form
class DietFormTest(unittest.TestCase):

    # Testing required field of daily calorie intake to not be blank
    def test_preferences_form_no_calories(self):
        # Filling a form with no daily calorie intake
        form = PreferencesForm(data={"daily_calorie_intake": None})

        # Checking that error is raised for the daily calorie intake field, which tells the user
        # that the field is required
        self.assertEqual(form.errors['daily_calorie_intake'], ['This field is required.'])

    # Testing valid preferences form saved without optional fields
    def test_preferences_form_valid(self):
        # Creating form with valid daily calories
        form = PreferencesForm(data={"daily_calorie_intake": 1200})

        # Checking that the form can be saved with the given that
        self.assertTrue(form.is_valid())

    # Testing whether optional fields show errors if available options aren't selected
    def test_invalid_optional_values(self):
        # Inputting a form with invalid excluded cuisine
        form = PreferencesForm(data={"daily_calorie_intake": 1200, "exclude_cuisines": "africaeeen"})
        self.assertEqual(form.errors['exclude_cuisines'], ['Please check if values match with the provided values.'])

        # Inputting a form with invalid diet
        form = PreferencesForm(data={"daily_calorie_intake": 1200, "diet": "gluten fre"})
        self.assertEqual(form.errors['diet'], ['Please check if values match with the provided values.'])

        # Inputting a form with invalid intolerance
        form = PreferencesForm(data={"daily_calorie_intake": 1200, "intolerance": "dayre"})
        self.assertEqual(form.errors['intolerance'], ['Please check if values match with the provided values.'])

    # Testing whether valid inputs for optional fields work as intended
    def test_valid_optional_values(self):
        # Inputting a form with valid optional fields
        form = PreferencesForm(data={"daily_calorie_intake": 1200, "exclude_cuisines": "african",
                                     "diet": "gluten free", "intolerance": "dairy"})
        self.assertTrue(form.is_valid())

    # Testing whether multiple values can be inputted by separating by comma
    # and whether capital letter can be used
    def test_capital_letter_and_comma_input(self):
        # Inputting a form with valid optional fields
        form = PreferencesForm(data={"daily_calorie_intake": 1200, "exclude_cuisines": "african,american",
                                     "diet": "gluten free, Vegeterian "})

        self.assertTrue(form.is_valid())

    # Testing the method which is used to separate the string by commas into array and decapitalize
    def test_separated_by_commas_method(self):
        # Inputting a valid form
        form = PreferencesForm(data={"daily_calorie_intake": 1200})

        # Testing whether the method will correctly return list of values which were separated by commmas
        # so that all of the components can be checked against possible values
        self.assertEqual(form.separate_by_commas('african, american, British,cajun,Caribbean'), ['african', 'american', 'british', 'cajun', 'caribbean'])

class DietViewTests(unittest.TestCase):

    def setUp(self) -> None:
        # Defining a django client to be able to test on it
        self.client = Client()

        # Creating an account so that user can log in
        self.a1 = Account(
            username='userusername1',
            email='userusername1@gmail.com'
        )
        # Setting password for the account
        self.a1.set_password('passwordSecret')
        # Saving the user into the database
        self.a1.save()
        # Creating progress for the user
        self.create_progress()

    def tearDown(self) -> None:
        a1 = Account.objects.get(username='userusername1')
        a1.delete()

    # Creating a progress, because a progress is required for a user
    def create_progress(self):
        # Creating a progress for the user so that they can access the dashboard
        self.progress = Progress(user=self.a1,
                                 starting_height=1.85,
                                 starting_weight=100,
                                 target_bmi=20)

        self.progress.initial_current_set()
        self.progress.save()

    # Testing whether the preferences form can be accessed by the user
    def test_preferences_form_valid(self):
        # Calling the login view, and passing valid parameters for the user
        response = self.client.post('/login/', {'username': 'userusername1', 'password': 'passwordSecret'}, follow=True)

        # Defining the url that the client will access (url to the form)
        url = "/account/dashboard/{}/set_preferences".format(response.context['user'].id)

        # Getting the response when the user submits the form
        response = self.client.get(url)

        # Checking if it was accessed fine
        self.assertEqual(response.status_code, 200)

        # Checking for the daily calorie intake field
        self.assertTrue(response.context['form']['daily_calorie_intake'])


#TODO
#   Tests

    # Testing whether the form saves the diet for the user
    def test_preferences_form_submit_valid(self):
    
        # Logging the client in as the account defined above
        response = self.client.post('/login/', {'username': 'userusername1', 'password': 'passwordSecret'}, follow=True)
    
        # Defining the url that the client will access (url to the form)
        url = "/account/dashboard/{}/set_preferences".format(self.a1.id)
    
        # Checking that the account does not have any diets at the moment
        diet = Diet.objects.filter(user=self.a1)
        self.assertEqual(len(diet), 0)
    
        # Getting the response when the user submits the form with valid data
        response = self.client.post(url, {'daily_calorie_intake': 1200, 'exclude_cuisines': 'British'}, follow=True)
    
        self.assertEqual(response.redirect_chain[0][0], '/account/dashboard/{}'.format(self.a1.id))
    
        # Trying to get the diet for the current user, to verify it was saved into the database through the form
        diet = Diet.objects.get(user=self.a1)
        self.assertEqual(diet.daily_calories, 1200)
        self.assertEqual(diet.exclude_cuisines, 'british')









