from django.test import TestCase
from django.db.utils import IntegrityError
from django.test import Client

from .models import Recipe
from account.models import Account
from diets.models import Diet
from progress.models import Progress

import unittest

# Testing recipe model
class RecipeModelTest(unittest.TestCase):

    # Testing whether there can be 2 recipes with identical name saved into the database
    def test_duplicate_name(self):
        # Two recipes with the same name
        recipe = Recipe(name='Name1', recipe_id=123041232312136543, meal_type='Lunch',
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        recipe2 = Recipe(name='Name1', recipe_id=123041232312136542, meal_type='Lunch',
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        # Saving the first recipe
        recipe.save()

        # Expecting an error on the second recipe as there is already one recipe with that name
        with self.assertRaises(IntegrityError) as context:
            recipe2.save()

        # Cleaning the recipe
        recipe.delete()

    # Testing whether two recipes with duplicate id can be saved
    def test_duplicate_id(self):
        # Defining two recipes with the same ids but different names
        recipe = Recipe(name='Name1', recipe_id=123041232312136542, meal_type='Lunch',
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        recipe2 = Recipe(name='Name2', recipe_id=123041232312136542, meal_type='Lunch',
                         image_link="videoUrl", ingredients='Ingredient list', servings=2,
                         summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                         carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)
        # Saving the first recipe
        recipe.save()

        # Expecting an error when saving the second recipe as there exists a recipe with that recipe_id already
        with self.assertRaises(IntegrityError) as context:
            recipe2.save()
        # Cleaning the database
        recipe.delete()

    # Testing that id is required to save the recipe
    def test_no_id(self):
        # Defining an invalid recipe, with recipe_id field set to None
        recipe = Recipe(name='Name1', recipe_id=None, meal_type='Lunch',
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        # Expecting an error when saving the recipe
        with self.assertRaises(IntegrityError) as context:
            recipe.save()

    # Testing saving a recipe without a name
    def test_no_name(self):
        # Making a recipe that has no name
        recipe = Recipe(name=None, recipe_id=123041232312136542, meal_type='Lunch',
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        # Expecting an error when saving the recipe
        with self.assertRaises(IntegrityError) as context:
            recipe.save()

    # Testing saving a recipe without a meal type
    def test_no_meal_type(self):
        # Making a recipe that has no meal type
        recipe = Recipe(name="Recipe Name", recipe_id=123041232312136542, meal_type=None,
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        # Expecting an error when saving the recipe
        with self.assertRaises(IntegrityError) as context:
            recipe.save()


    # TODO
    #   test
    def test_valid_meal_type(self):
        pass



    # Testing saving a valid recipe
    def test_valid_saving(self):
        # Making a valid recipe
        recipe = Recipe(name="Recipe Name", recipe_id=123041232312136542, meal_type="Lunch",
                        image_link="videoUrl", ingredients='Ingredient list', servings=2,
                        summary="Summary of the Recipe", source_link="sourceUrl", protein=30,
                        carbs=30, fats=30, calories=2000, saturated_fats=10, sugars=2)

        # Verifying that it does not exist in the database
        recipeQ = Recipe.objects.filter(name='Recipe Name')
        self.assertEqual(len(recipeQ), 0)

        # Saving the recipe
        recipe.save()

        # Showing that the recipe was found after saving it
        recipeQ = Recipe.objects.get(name='Recipe Name')
        self.assertEqual(recipeQ.recipe_id, 123041232312136542)
        recipe.delete()

# Class to test recipe views
class RecipeViewTests(unittest.TestCase):
    # Setting up the account as well as a recipe for testing
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

        self.client = Client()

    # Cleaning the database from the test data
    def tearDown(self) -> None:
        self.account.delete()
        self.diet.delete()
        self.recipe.delete()


    # Testing viewing the recipe
    def test_view_recipe(self):
        # Url to a recipe defined in a setup
        url = "/recipe/{}".format(self.recipe.id)
        # Getting the response from client accessing the url, recipe view
        response = self.client.get(url, follow=True)

        # Checking the status code
        self.assertEqual(response.status_code, 200)

        # Checking that the recipe that was accessed is the one we wanted
        self.assertEqual(response.context['recipe'].name, self.recipe.name)

    # Testing viewing a recipe that does not exist with user logged in
    def test_view_invalid_recipe_logged_in(self):
        # Logging the client into the system
        response = self.client.post("/login/", {'username': 'username1', 'password': 'password1'})

        # Url to a recipe that does not exist
        url = "/recipe/{}".format(100000000000)

        # Getting the response from client accessing the url, recipe view
        response = self.client.get(url, follow=True)

        # Verifying that the user that is logged in is redirected to the dashboard
        self.assertEqual(response.redirect_chain[0][0], '/account/dashboard/{}'.format(self.account.pk))
        self.assertEqual(response.redirect_chain[0][1], 302)

    # Testing viewing a recipe that does not exist with user logged out
    def test_view_invalid_recipe_logged_out(self):
        # Url to a recipe that does not exist
        url = "/recipe/{}".format(100000000000)

        # Getting the response from client accessing the url, recipe view
        response = self.client.get(url, follow=True)

        # Verifying that the logged out user that was redirected is taken to the home page
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
