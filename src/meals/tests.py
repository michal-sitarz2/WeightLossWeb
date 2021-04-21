from django.test import TestCase
from django.db.utils import IntegrityError
from django.test import Client

from .models import Meal
from .views import fill_days
from account.models import Account
from recipes.models import Recipe
from diets.models import Diet
from progress.models import Progress

import unittest
import datetime

# Class to test meal model
class MealModelTest(unittest.TestCase):
    # Setting up the account and recipes so that they can be linked via Meal object
    def setUp(self) -> None:
        # Making and saving an account
        self.account = Account(username='username1', email='user1@gmail.com')
        self.account.set_password('password1')
        self.account.save()

        # Making a diet for a user and saving it
        self.diet = Diet(user=self.account, daily_calories=2200)
        self.diet.save()

        # Making a random recipe that the user will have as their meal
        self.recipe = Recipe(name='Recipe Name', recipe_id=12304123231213, meal_type='Lunch',
                             image_link="videoUrl", ingredients='Ingredient list', servings=2,
                             summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                             carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        self.recipe.save()

    # Deleting all of the objects to not stay in the database
    def tearDown(self) -> None:
        self.diet.delete()
        self.account.delete()
        self.recipe.delete()

    # Testing that the meal cannot be saved without meal date
    def test_meal_no_date(self):
        # Making a meal without a date
        meal = Meal(diet=self.diet, recipe=self.recipe)

        # Expecting an Error when saving the meal without date
        with self.assertRaises(IntegrityError) as context:
            meal.save()

    # Testing that meal has to have a diet (in turn an account) that it is related to
    def test_meal_no_diet(self):
        # Setting a random date
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        # Making a meal without a diet
        meal = Meal(meal_date=date, recipe=self.recipe)

        # Expecting an Error to pop up
        with self.assertRaises(IntegrityError) as context:
            meal.save()

    # Testing that a meal cannot be saved without recipe, as it connects the diet/account with the recipe
    def test_meal_no_recipe(self):
        # Random date
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        # Making a meal without a recipe
        meal = Meal(diet=self.diet, meal_date=date)

        # Expecting an error when saving
        with self.assertRaises(IntegrityError) as context:
            meal.save()

    # Testing that a valid meal can be saved
    def test_valid_meal(self):
        # Defining a date and making a meal with all the required fields
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        meal = Meal(diet=self.diet, meal_date=date, recipe=self.recipe)

        # Checking that the specific diet(account) that was created in the setup
        # Does not have any recipes related to it, i.e. does not have any meals yet
        meals = len(Meal.objects.filter(diet=self.diet).filter(recipe=self.recipe))
        self.assertEqual(meals, 0)

        # Saving the newly made meal
        meal.save()

        # Verifying that there is a new meal saved into the database
        meals = len(Meal.objects.filter(diet=self.diet).filter(recipe=self.recipe))
        self.assertEqual(meals, 1)

    # Testing that upon diet deletion, meal is also deleted
    def test_delete_cascade_diet(self):
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        # Making and saving an account
        account = Account(username='username2', email='user2@gmail.com')
        account.set_password('password1')
        account.save()

        # Making and saving a diet
        diet = Diet(user=account, daily_calories=2200)
        diet.save()

        # Checking that there are no current meals in the database for the user
        self.assertEqual(len(Meal.objects.filter(diet=diet)), 0)

        # Making a meal and saving it for the user
        meal = Meal(diet=diet, meal_date=date, recipe=self.recipe)
        meal.save()

        # Checking that the meal is in the database
        self.assertEqual(len(Meal.objects.filter(diet=diet)), 1)

        # Deleting the diet plan for the user
        diet.delete()

        # Verifying that without the diet plan, the meals are also gone
        self.assertEqual(len(Meal.objects.filter(diet=diet)), 0)

        # Cleaning up the database by deleting the local account
        account.delete()

    # Testing that upon recipe deletion, meal is also deleted as a meal cannot exist without recipe
    def test_delete_cascade_recipe(self):
        date = datetime.datetime.today() + datetime.timedelta(days=1)

        # Making a recipe and saving it
        recipe = Recipe(name='Recipe Name 2', recipe_id=123041232312132, meal_type='Lunch',
                             image_link="videoUrl", ingredients='Ingredient list', servings=2,
                             summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                             carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        recipe.save()

        # Checking that there are no meals with that recipe before saving the meal
        self.assertEqual(len(Meal.objects.filter(recipe=recipe)), 0)

        # Saving the meal
        meal = Meal(diet=self.diet, meal_date=date, recipe=recipe)
        meal.save()

        # Checking that the meal was successfully saved into the database
        self.assertEqual(len(Meal.objects.filter(recipe=recipe)), 1)

        # Deleting the recipe that was related to the meal
        recipe.delete()
        # Veryfing that there are no meals asociated to that recipe anymore
        self.assertEqual(len(Meal.objects.filter(recipe=recipe)), 0)

    # Testing the output of the to string method
    def test_to_string_method(self):
        # Making a meal
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        meal = Meal(diet=self.diet, meal_date=date, recipe=self.recipe)

        # Expected output of the to string method
        check_str = "Recipe: Recipe Name (Lunch)\n" \
                "Diet: {}\nMeal Date: {}".format(self.diet.user.username, date.date())

        # Getting the to string method from the meal
        meal_str = str(meal)
        # Comparing the two
        self.assertEqual(meal_str, check_str)

# Class to test the meal views
class MealsViewTests(unittest.TestCase):

    # Setting up all the accounts and recipes required to test the views
    def setUp(self) -> None:
        # Making and saving an account
        self.account = Account(username='username1', email='user1@gmail.com')
        self.account.set_password('password1')
        self.account.save()

        progress = Progress(starting_height=1.85, starting_weight=100, user=self.account, target_bmi=20)
        progress.initial_current_set()
        progress.save()

        # Making a diet for a user and saving it
        self.diet = Diet(user=self.account, daily_calories=2200)
        self.diet.save()

        # Making a random recipe that the user will have as their meal
        self.recipe = Recipe(name='Recipe Name', recipe_id=12304123231213, meal_type='Lunch',
                             image_link="videoUrl", ingredients='Ingredient list', servings=2,
                             summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                             carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        self.recipe.save()

        # Making and saving a meal
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.meal = Meal(diet=self.diet, meal_date=date.date(), recipe=self.recipe)
        self.meal.save()

        # Making a django client to access urls
        self.client = Client()

    # Cleaning up after testing by deleting all the diets, accounts, recipes and meals
    def tearDown(self) -> None:
        self.diet.delete()
        self.account.delete()
        self.recipe.delete()
        self.meal.delete()


    # Testing whether once the recipe for a specific day is deleted, that it will be pushed back to the end of the meal plan
    def test_delete_and_save_later_meal(self):
        # Making a random recipe that the user will have as their meal
        recipe = Recipe(name='Recipe Name2', recipe_id=12304122233231213, meal_type='Lunch',
                             image_link="videoUrl", ingredients='Ingredient list', servings=2,
                             summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                             carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        recipe.save()

        # Making a meal which is 2 days in the future, in comparison to one already saved in the setup which is a day
        # into the future
        date = datetime.datetime.today() + datetime.timedelta(days=2)
        meal = Meal(diet=self.diet, meal_date=date.date(), recipe=self.recipe)
        meal.save()

        # Logging the client into the system
        response = self.client.post("/login/", {'username': 'username1', 'password': 'password1'})

        url = '/account/dashboard/{}/view_recipe_recommendations'.format(self.account.pk)
        response = self.client.get(url)

        # Making the client go to a link (on the website in form of a button) to delete the meal from the setup
        url = '/meal/delete/{}/{}/{}/{}'.format(self.recipe.id, self.meal.meal_date.day,
                                                self.meal.meal_date.month, self.meal.meal_date.year)
        # Getting the response
        response = self.client.get(url, follow=True)

        # As there was a recipe for the same meal type in the db two days from today, the new recipe should be saved
        # a day after it, hence 3 days into the future
        date = datetime.datetime.today() + datetime.timedelta(days=3)
        # Getting the newly saved recipe
        meal = Meal.objects.filter(diet=self.diet).get(meal_date=date.date())

        # Checking that the name of the recipe is the same as the one that was deleted
        self.assertEqual(meal.recipe.name, "Recipe Name")

        # Trying to get the recipe that was deleted
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        meal = Meal.objects.filter(diet=self.diet).filter(meal_date=date.date())

        # Proving that the recipe that was deleted is gone
        self.assertEqual(len(meal), 0)

        # Cleaning up the meals and recipes used in this test
        meal.delete()
        recipe.delete()


    # Testing deleting of a meal if it is the only meal of that type for the user
    def test_delete_with_one_meal(self):
        # Logging the client in
        response = self.client.post("/login/", {'username': 'username1', 'password': 'password1'})

        url = '/account/dashboard/{}/view_recipe_recommendations'.format(self.account.pk)
        response = self.client.get(url)

        # Making the client delete the meal from setup
        url = '/meal/delete/{}/{}/{}/{}'.format(self.recipe.id, self.meal.meal_date.day, self.meal.meal_date.month, self.meal.meal_date.year)
        response = self.client.get(url, follow=True)

        # Getting the new meal, which now is 2 days from today, as it is a day after the last one was deleted
        date = datetime.datetime.today() + datetime.timedelta(days=2)
        meal = Meal.objects.filter(diet=self.diet).get(meal_date=date.date())

        # Proving that it is the same as the one that was just deleted
        self.assertEqual(meal.recipe.name, "Recipe Name")

        # Verifying that the other on was in fact deleted
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        meal = Meal.objects.filter(diet=self.diet).filter(meal_date=date.date())
        self.assertEqual(len(meal), 0)

        # Cleaning up meals used
        meal.delete()

        # Checking that correct message was sent with the request
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The meal was successfully completed!")

    # Testing when deleting fails
    def test_delete_fail(self):
        # Logging the user into the system
        response = self.client.post("/login/", {'username': 'username1', 'password': 'password1'})

        url = '/account/dashboard/{}/view_recipe_recommendations'.format(self.account.pk)
        response = self.client.get(url)

    
        url = '/meal/delete/{}/{}/{}/{}'.format(self.recipe.id - 1, self.meal.meal_date.day, self.meal.meal_date.month,
                                                self.meal.meal_date.year)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.redirect_chain[0][0], "/account/dashboard/{}".format(self.account.id))
        self.assertEqual(response.redirect_chain[0][1], 302)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "The meal couldn't be checked off.")


    def test_filling_days_for_meals(self):
        date = datetime.datetime.today()
        date2 = datetime.datetime.today() + datetime.timedelta(days=1)

        dict_meals1 = {}
        dict_meals2 = {}
        # Meals for one meal type (e.g. lunch)
        meal1 = Meal(diet=self.diet, meal_date=date, recipe=self.recipe)
        meal1.save()
        meal2 = Meal(diet=self.diet, meal_date=date2, recipe=self.recipe)
        meal2.save()

        recipe2 = Recipe(name='Recipe Name3', recipe_id=1230412223323121213, meal_type='Dinner',
                         image_link="videoUrl", ingredients='Ingredient list', servings=2,
                         summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                         carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        recipe2.save()

        # Meals for a second meal type (e.g. dinner)
        meal3 = Meal(diet=self.diet, meal_date=date, recipe=recipe2)
        meal3.save()
        meal4 = Meal(diet=self.diet, meal_date=date2, recipe=recipe2)
        meal4.save()

        # Dictionary of meals where key is the date and the value is the meal
        dict_meals1[date] = meal1
        dict_meals1[date2] = meal2

        dict_meals2[date] = meal3
        dict_meals2[date2] = meal4

        days = {}


        days = fill_days(days, dict_meals1)
        days = fill_days(days, dict_meals2)

        self.assertEqual(len(days[date]), 2)
        self.assertEqual(days[date][0].recipe.meal_type, "Lunch")
        self.assertEqual(days[date][1].recipe.meal_type, "Dinner")


        self.assertEqual(len(days[date2]), 2)
        self.assertEqual(days[date2][0].recipe.meal_type, "Lunch")
        self.assertEqual(days[date2][1].recipe.meal_type, "Dinner")

        meal1.delete()
        meal2.delete()
        meal3.delete()
        meal4.delete()
        recipe2.delete()


    def test_show_meals_not_authenticated(self):
        url = '/account/dashboard/{}/view_recipe_recommendations'.format(self.account.pk)

        response = self.client.get(url, follow=True)

        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)


    def test_show_meals(self):
        date = datetime.datetime.today()
        date2 = datetime.datetime.today() + datetime.timedelta(days=1)

        meal1 = Meal(diet=self.diet, meal_date=date, recipe=self.recipe)
        meal1.save()
        meal2 = Meal(diet=self.diet, meal_date=date2, recipe=self.recipe)
        meal2.save()

        recipe2 = Recipe(name='Recipe Name3', recipe_id=1230412223323121213, meal_type='Dinner',
                         image_link="videoUrl", ingredients='Ingredient list', servings=2,
                         summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                         carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        recipe2.save()

        # Meals for a second meal type (e.g. dinner)
        meal3 = Meal(diet=self.diet, meal_date=date, recipe=recipe2)
        meal3.save()
        meal4 = Meal(diet=self.diet, meal_date=date2, recipe=recipe2)
        meal4.save()

        response = self.client.post("/login/", {'username': 'username1', 'password': 'password1'})

        url = '/account/dashboard/{}/view_recipe_recommendations'.format(self.account.pk)
        response = self.client.get(url, follow=True)

        self.assertEqual(len(dict(response.context['days']).keys()), 3)

        self.assertEqual(list(dict(response.context['days']).keys())[0].date(), datetime.datetime.today().date())

        meal1.delete()
        meal2.delete()
        meal3.delete()
        meal4.delete()
        recipe2.delete()


