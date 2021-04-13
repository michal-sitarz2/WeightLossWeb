from django.shortcuts import render, redirect
import requests, json, random
from random import randint

def choose_meals_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")

    context = {}

    # Information the user has specified for preferences with their recipes
    user = request.user.diet
    exclude_cuisines = user.exclude_cuisines
    diet = user.diets
    intolerance = user.intolerances
    exclude_ingredients = user.exclude_ingredients
    daily_calories = user.daily_calories

    # As per research, the calorie intake per day should be at least 1200,
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
                   'minCalories': main_course_cut-100, 'maxCalories': main_course_cut+100,
                   'number': 28, 'apiKey': 'db078d8202d840b78592794720def365'}

    # Getting the response from the API
    response = requests.request("GET", url, params=querystring)

    # Converting the information to JSON so that it can be used as a dictionary
    main_courses_data = json.loads(response.text)


    #### Useful to use when testing. Uncomment the first one when calling the api for the first time per session.
    #### And then comment the api calls and comment out the data variable to read from session.
    ###request.session['main_courses_data'] = main_courses_data
    ###breakfast_data = request.session['breakfast_data']

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
    #print(breakfast_data)
    context['breakfast'] = breakfast_dict

    snack_dict = get_recipe_information(snack_data, 14)
    context['snack'] = snack_dict

    return render(request, "meals/list_recipes.html", context)


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



'''
type (meal type) =>
main course, breakfast, snack

For filtering: minCarbs, maxCarbs, minProtein, maxProtein, minCalories, maxCalories, minFat, maxFat
healthScore
'''