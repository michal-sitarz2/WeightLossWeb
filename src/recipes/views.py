from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferencesForm
from .forms import SearchRecipeForm
import requests
import json

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

# The following two methods are for a search imput that looks through the API and list recepies based on a search. 
# The Goal is to make it look better!

def spoonacular_api_search_form(request):
    if request.method == 'POST':
        form = SearchRecipeForm(request.POST)
        if form.is_valid():
            request.session['search_engine'] = form.cleaned_data
            return redirect('/search/result')
    else:
        form = SearchRecipeForm()

    return render(request, 'recipes/spoonacular_search_form.html', {'form': form})

def spoonacular_api_search_view(request):

    context = {}
    
    search_query = request.session['search_engine']['search_query']

    url = "https://api.spoonacular.com/"

    complexSearch = "recipes/complexSearch"
    findByIngredients = "recipes/findByIngredients"
    
    querystring = {"query": search_query, 'addRecipeInformation': True, 'number': 10, 'apiKey': '64dadb7cfd724991b7ea9987c4685790'}
    response = requests.request("GET", url + complexSearch, params=querystring)
    content = json.loads(response.text)

    context['response'] = response
    context['search_query'] = search_query
    context['content'] = content['results']
    # context['ingredients'] = content['results']['ingredients']
    # for r in content['results']:

    #     context['ingredientName'] = r['ingredients'].get('name')

    return render(request, "recipes/spoonacular_search_view.html", context)