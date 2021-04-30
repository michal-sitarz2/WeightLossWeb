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
from django.contrib import messages

# View which is used to set preferences and display the form
def set_preferences_form(request, pk):
    # Checking if the request to the page was POST
    if request.method == 'POST':
        # If it was POST, we want to get the form that was submitted
        form = PreferencesForm(request.POST)
        # Checking if the form that was submitted is valid
        if form.is_valid():
            # Getting the data that was inputted into the form
            ex_cu = form.cleaned_data['exclude_cuisines'].lower()
            ex_ing = form.cleaned_data['exclude_ingredients'].lower()
            diets = form.cleaned_data['diet'].lower()
            intolerances = form.cleaned_data['intolerance'].lower()
            daily_calories = form.cleaned_data['daily_calorie_intake']

            # Trying to get the diet for the user, and if it exists, the current preferences will be updated
            try:
                diet = Diet.objects.get(user=request.user)
                diet.exclude_cuisines = ex_cu
                diet.diets = diets
                diet.intolerances = intolerances
                diet.exclude_ingredients = ex_ing
                diet.daily_calories = daily_calories

            # If the user was not found, new diet is created
            except Exception as e:
                diet = Diet(user=request.user,
                            exclude_cuisines=ex_cu,
                            exclude_ingredients=ex_ing,
                            diets=diets,
                            intolerances=intolerances,
                            daily_calories=daily_calories)
            # Saving the diet into the database
            diet.save()


            # Calls a method that creates meals for the user
            create_meals(request)

            # Redirecting the user to the meal plan
            return redirect('view_recipe_recommendations', pk)

    # If the GET request was made, setting the form
    form = PreferencesForm()
    # Returning the template for setting the preferences with the form
    return render(request, 'diets/set_preferences_form.html', {'form': form})


# Function used to create the meals for the user
def create_meals(request):
    # If user has no meals allocated yet
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
        if (daily_calories - 500) >= 2300:
            total_calories = daily_calories - 500
        else:
            total_calories = 2300

        # Setting the breakfast to be around 20% of daily calorie intake
        breakfast_cut = total_calories * 0.2
        # Setting the main courses to be around 40% of daily intake (around because it is the average, it will be used
        # to define min and max calories range)
        main_course_cut = total_calories * 0.4
        # Setting the snacks to be only 10% of the daily calories intake
        snacks_cut = total_calories * 0.1

        # URL to filter lunch and dinner recipes
        url = "https://api.spoonacular.com/recipes/complexSearch"
        # Creating a request for main courses which will return a JSON file of recipes matching this query
        querystring = {'excludeCuisines': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                       'excludeIngredients': exclude_ingredients, 'type': 'main course', 'addRecipeNutrition': True,
                       'minCalories': main_course_cut - 200, 'maxCalories': main_course_cut + 200,
                       'number': 28, 'apiKey': 'db078d8202d840b78592794720def365'}

        # Getting the response from the API
        response = requests.request("GET", url, params=querystring)

        # Converting the information to JSON so that it can be used as a dictionary
        main_courses_data = json.loads(response.text)

        # Changing the query string to make a request for breakfast recipes
        querystring['excludeCuisines'] = ''
        querystring['minCalories'] = breakfast_cut - 100
        querystring['maxCalories'] = breakfast_cut + 100
        querystring['number'] = 14
        querystring['type'] = 'breakfast'

        # Getting the response from the API
        response = requests.request("GET", url, params=querystring)
        # Converting the information to JSON so that it can be used as a dictionary
        breakfast_data = json.loads(response.text)

        # Changing the query string to make a request for snacks
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

        # Getting the information from the API response and limiting it to 2 recipes for breakfasts for 2 weeks
        breakfast_dict = get_recipe_information(breakfast_data, 2)
        context['breakfast'] = breakfast_dict

        # Getting the snacks for 2 weeks
        snack_dict = get_recipe_information(snack_data, 14)
        context['snack'] = snack_dict


        # Calling a function that will save the meals for the user for each meal type
        save_user_meal(context['breakfast'], user, 'breakfast')
        save_user_meal(context['main_courses'], user, 'main')
        save_user_meal(context['snack'], user, 'snack')


# Method to save the recipe for the user
def save_user_meal(recipes, diet, meal_type):
    # Counters for lunch and dinner as they are placed in one recipes dictionary (need to separate them)
    lunch = 0
    dinner = 0

    # Looping through the recipes in the recipes dictionary
    for i, recipe in enumerate(recipes.values()):
        # Getting the information for each recipe (all info the same order from the get_recipe_information function)
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

        # Checking if the meal is breakfast
        if(meal_type=='breakfast'):
            meal = 'breakfast'
        # Checking if the meal is main course (need to split them into lunch and dinner)
        elif(meal_type=='main'):
            # First half of the found recipes will be lunches
            if(i < int(len(recipes)/2)):
                meal = 'lunch'
                lunch += 1
            # The other half will be dinners
            elif(i >= int(len(recipes)/2)):
                meal = 'dinner'
                dinner += 1

        # Finally, checking if the meal is a snack
        elif(meal_type=='snack'):
            meal = 'snack'

        # Checking if the recipe is already in the database
        try:
            # If the recipe with the spoonacular recipe id and the meal type will not be found exception will be thrown.
            # The problem is that the recipe can be in the database already but have a different meal_type (e.g. lunch
            # but we want it as a dinner now) hence we need to check both the recipe id and meal type.
            recipe = Recipe.objects.get(recipe_id=id).get(meal_type=meal)
        except:
            # If the recipe does not exist, new one will be created.
            recipe = Recipe(name=title, recipe_id=id, meal_type=meal, image_link=image, ingredients=ingredients,
                            servings=servings, summary=summary, source_link=source_url, calories=calories, fats=fats,
                            carbs=carbs, sugars=sugar, saturated_fats=sat_fat, protein=protein)
            # Saving the recipe
            recipe.save()

        # Checking the meal type
        if (meal_type == 'snack'):
            # Creating dates for every day from tomorrow to the length of how many recipes were found
            delta = i + 1
            date = datetime.date.today() + timedelta(days=delta)
            # Saving the meal for the user into the database with the recipe
            meal = Meal(meal_date=date, diet=diet, recipe=recipe)
            meal.save()

        # Saving Lunches and Dinners
        if(meal_type=='main'):
            # Setting the counter for the dates, depending whether the meal is lunch or dinner
            # Because we want to add lunches and dinners day by day, we need two separate counters for them
            if(meal=='lunch'):
                counter = lunch
            else:
                counter = dinner

            # Getting the next date for lunch or dinner
            date = datetime.date.today() + timedelta(days=counter)
            # Saving the meal
            meal = Meal(meal_date=date, diet=diet, recipe=recipe)
            meal.save()

        # Saving breakfast meals for the upcoming two weeks
        if(meal_type=="breakfast"):
            # We expect at least one breakfast (max 2), first breakfast will be put for the whole upcoming week
            if(i==0):
                # Getting the date from tomorrow
                current_date = datetime.date.today() + timedelta(days=1)
                # Getting the date a week after tomorrow
                end_date = current_date + timedelta(days=7)
                # Looping through the range of those days (that week)
                while current_date < end_date:
                    # Saving the breakfast for that week
                    meal = Meal(meal_date=current_date, diet=diet, recipe=recipe)
                    meal.save()
                    # Incrementing the current date
                    current_date += timedelta(days=1)
            # If there are two breakfasts, second will be put for the week after the first one
            else:
                # Getting the date that is after the first week of the meal plan
                current_date = datetime.date.today() + timedelta(days=8)
                # Getting the week after the above date
                end_date = current_date + timedelta(days=7)
                # Looping through the range of those dates, i.e. the 2 week of the meal plan.
                while current_date < end_date:
                    # Saving the meal into the database
                    meal = Meal(meal_date=current_date, diet=diet, recipe=recipe)
                    meal.save()
                    # Incrementing the date
                    current_date += timedelta(days=1)

# Helper method used to get the information from the json file returned by the API
def get_recipe_information(data, limit):
    # Defining a list which will hold the recipes
    recipes = []

    # Doing try-catch as there might not be results when daily quota is exceeded
    try:
        # Iterating through all the recipes that were returned
        for i, recipe in enumerate(data['results']):
            # If we wanted to get more recipes from the API, and limit them, the limit variable would be used
            # to stop when we have enough recipes
            if(i == limit):
                break

            # Making the recipes list, a list of lists
            recipes.append([])
            # Getting the title from the json
            recipes[i].append(recipe['title'])
            # Getting the id from the json
            recipes[i].append(recipe['id'])
            # Getting the health score from the json
            recipes[i].append(recipe['healthScore'])
            # Getting the servings from the json
            recipes[i].append(recipe['servings'])

            # Getting the important nutritional information from the json given by the api
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

            # Getting the image link
            recipes[i].append(recipe['image'])
            # Getting the link for the recipe
            recipes[i].append(recipe['sourceUrl'])
            # Getting the summary of the recipe
            recipes[i].append(recipe['summary'])

            # Making a string of ingredients used for the recipe
            ingredient_str = ""
            # Iterating through the ingredients list and appending it to the ingredients string.
            for ingredient in recipe['nutrition']['ingredients']:
                ingredient_str += "{} ({} {}), ".format(ingredient['name'], str(ingredient['amount']), ingredient['unit'])

            ingredient_str = ingredient_str[:-2].capitalize()

            # Appending the string to the recipes list
            recipes[i].append(ingredient_str)

        # Shuffling the recipes
        random.shuffle(recipes)

        # Out of the list of list, making a dictionary
        recipes_dict = {}
        for i, recipe in enumerate(recipes):
            i = str(i)
            recipes_dict[i] = recipe

    # If there were no results returned take user to home page and let them know they can't use the system today
    except:
        messages.error("There are no more recipes available today.")
        return redirect('/')

    # Returning the dictionary of recipes
    return recipes_dict
