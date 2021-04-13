from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferencesForm
from .models import Diet
import requests
import json

# Create your views here.
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
            return redirect('/account/dashboard/{}'.format(pk))
    else:
        form = PreferencesForm()

    return render(request, 'diets/set_preferences_form.html', {'form': form})

def view_recipe_preferences_view(request, pk):
    pass
#     if not request.user.is_authenticated:
#         return redirect("/")
#
#     context = {}
#
#     # Information the user has specified for preferences with their recipes
#     user = request.user.diet
#     exclude_cuisines = user.exclude_cuisines
#     diet = user.diets
#     intolerance = user.intolerances
#     exclude_ingredients = user.exclude_ingredients
#     daily_calories = user.daily_calories
#
#     # As per research, the calorie intake per day should be at least 1200,
#     # but it is relative to person's current calorie intake (hence decrease their calorie intake
#     # by 500 calories to help them loose around 0.5-1.0 kg weekly)
#     if (daily_calories-500) >= 1200:
#         total_calories = daily_calories-500
#     else:
#         total_calories = 1300
#
#
#     # URL to filter a recipes
#     url = "https://api.spoonacular.com/recipes/complexSearch"
#     querystring = {'excludeCuisine': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
#                    'excludeIngredients': exclude_ingredients, 'addRecipeNutrition': True, 'number':50,
#                    'apiKey': 'db078d8202d840b78592794720def365'}
#
#     # Getting the response from the API
#     response = requests.request("GET", url, params=querystring)
#
#     # Converting the information to JSON so that it can be used as a dictionary
#     data = json.loads(response.text)
#
#     # Not saving it to the database yet, hence saved to session for now
#     request.session['recipe_information'] = data
#     #data = request.session['recipe_information']
#
#
#     context['recipe_information'] = data['results'][0]
#     recipe = data['results'][0]
#
#     #print(recipe['dishTypes'])
#
#     # Calories
#     context['calories'] = recipe['nutrition']['nutrients'][0]
#     # Fats
#     context['fats'] = recipe['nutrition']['nutrients'][1]
#     # Saturated Fats
#     context['saturated_fats'] = recipe['nutrition']['nutrients'][2]
#     # Carbs
#     context['carbs'] = recipe['nutrition']['nutrients'][3]
#     # Sugar
#     context['sugars'] = recipe['nutrition']['nutrients'][5]
#     # Protein
#     context['protein'] = recipe['nutrition']['nutrients'][8]
#
#     # Ingredients
#     # Calling the API to retrieve the ingredients needed for the recipe, based on recipe's ID
#     url = "https://api.spoonacular.com/recipes/{}/ingredientWidget.json".format(recipe['id'])
#
#     querystring = {'apiKey': 'db078d8202d840b78592794720def365'}
#     ingredients = requests.request("GET", url, params=querystring)
#
#     request.session['ingredients'] = ingredients
#
#     ingredients = json.loads(ingredients.text)
#     context['ingredients'] = ingredients
#     request.session['ingredients'] = ingredients
#
#     ingredients = request.session['ingredients']
#     for ingredient in ingredients['ingredients']:
#         print(ingredient['name'], str(ingredient['amount']['metric']['value']),ingredient['amount']['metric']['unit'])
#
#     return render(request, "diets/view_recipe_preferences.html", context)


