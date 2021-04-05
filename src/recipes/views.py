from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferencesForm
import requests

def set_preferences_form(request, pk):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            request.session['preferences'] = form.cleaned_data
            return redirect('/account/dashboard/{}'.format(pk))
    else:
        form = PreferencesForm()

    return render(request, 'recipes/set_preferences_form.html', {'form': form})

def view_recipe_preferences_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")

    context = {}

    exclude_cuisines = request.session['preferences']['exclude_cuisines']
    diet = request.session['preferences']['diet']
    intolerance = request.session['preferences']['intolerance']
    exclude_ingredients = request.session['preferences']['exclude_ingredients']

    url = "https://api.spoonacular.com/recipes/complexSearch"
    querystring = {'excludeCuisine': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                   'excludeIngredients': exclude_ingredients, 'addRecipeNutrition': True, 'number': 7, 'apiKey': 'db078d8202d840b78592794720def365'}
    response = requests.request("GET", url, params=querystring)
    context['response'] = response

    return render(request, "recipes/view_recipe_preferences.html", context)

# def spoonacular_api_search_view(request):
#     pass
    # context = {}
    #
    # url = "https://api.spoonacular.com/recipes/complexSearch"
    #
    # querystring = {"query": "Chicken with Rice", 'apiKey': 'db078d8202d840b78592794720def365'}
    # response = requests.request("GET", url, params=querystring)
    #
    # context['response'] = response
    # return render(request, "recipes/spoonacular_search_view.html", context)