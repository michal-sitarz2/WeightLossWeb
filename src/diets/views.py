from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferencesForm
from .models import Diet
import requests, json, random
from random import randint
from recipes.models import Recipe
from meals.models import Meal
from datetime import date, datetime, timedelta
import datetime


def set_preferences_form(request, pk):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            ex_cu = form.cleaned_data['exclude_cuisines'].lower()
            ex_ing = form.cleaned_data['exclude_ingredients'].lower()
            diets = form.cleaned_data['diet'].lower()
            intolerances = form.cleaned_data['intolerance'].lower()
            daily_calories = form.cleaned_data['daily_calorie_intake']

            try:
                diet = Diet.objects.get(user=request.user)
                diet.exclude_cuisines = ex_cu
                diet.diets = diets
                diet.intolerances = intolerances
                diet.exclude_ingredients = ex_ing
                diet.daily_calories = daily_calories

            except Exception as e:
                diet = Diet(user=request.user,
                            exclude_cuisines=ex_cu,
                            exclude_ingredients=ex_ing,
                            diets=diets,
                            intolerances=intolerances,
                            daily_calories=daily_calories)

            diet.save()


            # Calls a method that creates meals for the user
            create_meals(request)

            return redirect('/account/dashboard/{}'.format(pk))
    else:
        form = PreferencesForm()

    return render(request, 'diets/set_preferences_form.html', {'form': form})



def create_meals(request):
    # If user has no meals allocated
    if not Meal.objects.filter(diet=request.user.diet):
        context = {}

        # Information the user has specified for preferences with their recipes
        user = request.user.diet
        exclude_cuisines = user.exclude_cuisines
        diet = user.diets
        intolerance = user.intolerances
        exclude_ingredients = user.exclude_ingredients
        daily_calories = user.daily_calories

        # According to research, the calorie intake per day should be at least 1200,
        # but it is relative to person's current calorie intake (hence decrease their calorie intake
        # by 500 calories to help them loose around 0.5-1.0 kg weekly)
        if (daily_calories - 500) >= 2000:
            total_calories = daily_calories - 500
        else:
            total_calories = 2000

        breakfast_cut = total_calories * 0.2
        main_course_cut = total_calories * 0.35
        snacks_cut = total_calories * 0.1

        # URL to filter lunch and dinner recipes
        url = "https://api.spoonacular.com/recipes/complexSearch"
        querystring = {'excludeCuisines': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                       'excludeIngredients': exclude_ingredients, 'type': 'main course', 'addRecipeNutrition': True,
                       'minCalories': main_course_cut - 100, 'maxCalories': main_course_cut + 100,
                       'number': 28, 'apiKey': 'db078d8202d840b78592794720def365'}

        # Getting the response from the API
        response = requests.request("GET", url, params=querystring)

        # Converting the information to JSON so that it can be used as a dictionary
        main_courses_data = json.loads(response.text)

        # Breakfast Recipes
        querystring['excludeCuisines'] = ''
        querystring['minCalories'] = breakfast_cut - 100
        querystring['maxCalories'] = breakfast_cut + 100
        querystring['number'] = 14
        querystring['type'] = 'breakfast'

        # Getting the response from the API
        response = requests.request("GET", url, params=querystring)
        # Converting the information to JSON so that it can be used as a dictionary
        breakfast_data = json.loads(response.text)

        # Snacks Recipes
        querystring['excludeCuisines'] = ''
        querystring['minCalories'] = snacks_cut - 100
        querystring['maxCalories'] = snacks_cut + 50
        querystring['type'] = 'snack'

        # Getting the response from the API
        response = requests.request("GET", url, params=querystring)
        # Converting the information to JSON so that it can be used as a dictionary
        snack_data = json.loads(response.text)

        # Getting the information from the API response and limiting it to 28 recipes for lunch and dinner
        # 28 = 14 * 2, 14 days (2 weeks), 2 meals per day (lunch and dinner)
        main_courses_dict = get_recipe_information(main_courses_data, 28)
        context['main_courses'] = main_courses_dict

        # Getting the information from the API response and limiting it to 2 recipes for breakfasts
        # For 2 weeks
        breakfast_dict = get_recipe_information(breakfast_data, 2)
        context['breakfast'] = breakfast_dict

        snack_dict = get_recipe_information(snack_data, 14)
        context['snack'] = snack_dict

        ### Save for user to the DB
        save_user_meal(context['breakfast'], user, 'breakfast')
        save_user_meal(context['main_courses'], user, 'main')
        save_user_meal(context['snack'], user, 'snack')


# Method to save the recipe for the user
def save_user_meal(recipes, diet, meal_type):
    size = len(recipes.values())
    for i, recipe in enumerate(recipes.values()):
        title = recipe[0]
        id = recipe[1]
        servings = recipe[3]
        calories = float(recipe[4].split(" ")[0])
        fats = float(recipe[5].split(" ")[0])
        sat_fat = float(recipe[6].split(" ")[0])
        carbs = float(recipe[7].split(" ")[0])
        sugar = float(recipe[8].split(" ")[0])
        protein = float(recipe[9].split(" ")[0])
        image = recipe[10]
        source_url = recipe[11]
        summary = recipe[12]
        ingredients = recipe[13]

        if(meal_type=='breakfast'):
            meal = 'breakfast'
        elif(meal_type=='main'):
            if(i<size/2):
                meal = 'lunch'
            else:
                meal = 'dinner'
        elif(meal_type=='snack'):
            meal = 'snack'

        # Checking if the recipe is already in the database
        try:
            recipe = Recipe.objects.get(recipe_id=id)
        except:
            recipe = Recipe(name=title, recipe_id=id, meal_type=meal, image_link=image, ingredients=ingredients,
                            servings=servings, summary=summary, source_link=source_url, calories=calories, fats=fats,
                            carbs=carbs, sugars=sugar, saturated_fats=sat_fat, protein=protein)
            recipe.save()

        if (meal_type == 'snack'):
            delta = (i % 14) + 1
            date = datetime.date.today() + timedelta(days=delta)
            meal = Meal(meal_date=date, diet=diet, recipe=recipe)
            meal.save()

        ### Saving Lunches and Dinners
        if(meal_type=='main'):
            delta = (i % 14) + 1
            date = datetime.date.today() + timedelta(days=delta)
            meal = Meal(meal_date=date, diet=diet, recipe=recipe)
            meal.save()

        ### Saving breakfast meals for the upcoming two weeks
        if(meal_type=="breakfast"):
            if(i==0):
                current_date = datetime.date.today() + timedelta(days=1)
                end_date = current_date + timedelta(days=7)
                while current_date < end_date:
                    meal = Meal(meal_date=current_date, diet=diet, recipe=recipe)
                    meal.save()
                    current_date += timedelta(days=1)
            else:
                current_date = datetime.date.today() + timedelta(days=8)
                end_date = current_date + timedelta(days=7)
                while current_date < end_date:
                    meal = Meal(meal_date=current_date, diet=diet, recipe=recipe)
                    meal.save()
                    current_date += timedelta(days=1)

def get_recipe_information(data, limit):
    recipes = []
    for i, recipe in enumerate(data['results']):
        if(i == limit):
            break

        recipes.append([])
        recipes[i].append(recipe['title'])
        recipes[i].append(recipe['id'])
        recipes[i].append(recipe['healthScore'])
        recipes[i].append(recipe['servings'])

        # Calories
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][0]['amount']) + " " + recipe['nutrition']['nutrients'][0]['unit'])
        # Fats
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][1]['amount']) + " " + recipe['nutrition']['nutrients'][1]['unit'])
        # Saturated Fats
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][2]['amount']) + " " + recipe['nutrition']['nutrients'][2]['unit'])
        # Carbs
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][3]['amount']) + " " + recipe['nutrition']['nutrients'][3]['unit'])
        # Sugar
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][5]['amount']) + " " + recipe['nutrition']['nutrients'][5]['unit'])
        # Protein
        recipes[i].append(
            str(recipe['nutrition']['nutrients'][8]['amount']) + " " + recipe['nutrition']['nutrients'][8]['unit'])

        recipes[i].append(recipe['image'])
        recipes[i].append(recipe['sourceUrl'])

        recipes[i].append(recipe['summary'])

        ingredient_str = ""
        for ingredient in recipe['nutrition']['ingredients']:
            ingredient_str += "{} ({} {}), ".format(ingredient['name'], str(ingredient['amount']), ingredient['unit'])

        ingredient_str = ingredient_str[:-2].capitalize()

        recipes[i].append(ingredient_str)

    # Shuffling the recipes
    random.shuffle(recipes)

    recipes_dict = {}
    for i, recipe in enumerate(recipes):
        i = str(i)
        recipes_dict[i] = recipe

    return recipes_dict
