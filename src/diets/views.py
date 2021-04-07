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
            # request.session['preferences'] = form.cleaned_data
            ex_cu = form.cleaned_data['exclude_cuisines']
            ex_ing = form.cleaned_data['exclude_ingredients']
            diets = form.cleaned_data['diet']
            intolerances = form.cleaned_data['intolerance']
            try:
                diet = Diet.objects.get(user=request.user)
                diet.exclude_cuisines = ex_cu
                diet.diets = diets
                diet.intolerances = intolerances
            except Exception as e:
                diet = Diet(user=request.user, total_energy=0, total_protein=0, total_carbs=0, total_fats=0,
                            exclude_cuisines=ex_cu,
                            exclude_ingredients=ex_ing,
                            diets=diets,
                            intolerances=intolerances)

            diet.save()
            return redirect('/account/dashboard/{}'.format(pk))
    else:
        form = PreferencesForm()

    return render(request, 'diets/set_preferences_form.html', {'form': form})

def view_recipe_preferences_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")

    context = {}

    # Information the user has specified for preferences with their recipes
    user = request.user.diet
    exclude_cuisines = user.exclude_cuisines
    diet = user.diets
    intolerance = user.intolerances
    exclude_ingredients = user.exclude_ingredients

    # URL to filter a recipe (number set to 1 at the moment)
    url = "https://api.spoonacular.com/recipes/complexSearch"
    querystring = {'excludeCuisine': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                   'excludeIngredients': exclude_ingredients, 'addRecipeNutrition': True, 'number':1, 'apiKey': 'db078d8202d840b78592794720def365'}
    # Getting the response from the API
    response = requests.request("GET", url, params=querystring)

    # Converting the information to JSON so that it can be used as a dictionary
    data = json.loads(response.text)

    # Not saving it to the database yet, hence saved to session for now
    request.session['recipe_information'] = data

    context['recipe_information'] = data['results'][0]
    recipe = data['results'][0]

    # # Title
    # print(recipe['title'])
    # # Image Link
    # print(recipe['image'])
    # # Servings
    # print(recipe['servings'])
    # # Recipe ID
    # print(recipe['id'])

    # Calories
    context['calories'] = recipe['nutrition']['nutrients'][0]
    # Fats
    context['fats'] = recipe['nutrition']['nutrients'][1]
    # Saturated Fats
    context['saturated_fats'] = recipe['nutrition']['nutrients'][2]
    # Carbs
    context['carbs'] = recipe['nutrition']['nutrients'][3]
    # Sugar
    context['sugars'] = recipe['nutrition']['nutrients'][5]
    # Protein
    context['protein'] = recipe['nutrition']['nutrients'][8]


    # Ingredients
    # Calling the API to retrieve the ingredients needed for the recipe, based on recipe's ID
    url = "https://api.spoonacular.com/recipes/{}/ingredientWidget.json".format(recipe['id'])

    querystring = {'apiKey': 'db078d8202d840b78592794720def365'}
    ingredients = requests.request("GET", url, params=querystring)

    request.session['ingredients'] = ingredients

    ingredients = json.loads(ingredients.text)
    context['ingredients'] = ingredients
    request.session['ingredients'] = ingredients

    ingredients = request.session['ingredients']
    for ingredient in ingredients['ingredients']:
        print(ingredient['name'], str(ingredient['amount']['metric']['value']),ingredient['amount']['metric']['unit'])

    return render(request, "diets/view_recipe_preferences.html", context)