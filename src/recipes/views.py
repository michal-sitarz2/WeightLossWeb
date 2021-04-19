from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchRecipeForm
import requests
import json

from .models import Recipe


# View a recipe
def view_recipe(request, recipe_id):
    context = {}

    recipe = Recipe.objects.filter(id=recipe_id)
    context['recipe'] = recipe[0]

    return render(request, 'recipes/view_recipe.html', context)

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

    return render(request, 'spoonacular_search_form.html', {'form': form})

def spoonacular_api_search_view(request):

    context = {}
    
    search_query = request.session['search_engine']['search_query']

    url = "https://api.spoonacular.com/"

    complexSearch = "recipes/complexSearch"
    findByIngredients = "recipes/findByIngredients"
    
    querystring = {"query": search_query, 'addRecipeInformation': True, 'number': 10, 'apiKey': '64dadb7cfd724991b7ea9987c4685790'}
    response = requests.request("GET", url + complexSearch, params=querystring)
    content = json.loads(response.text)
    # recipe = content['results']

    context['response'] = response
    context['search_query'] = search_query
    context['content'] = content['results']
    # context['ingredients'] = recipe['ingredients']
    # context['ingredients'] = content['results']['ingredients']
    # for r in content['results']:

    #     context['ingredientName'] = r['ingredients'].get('name')

    return render(request, "spoonacular_search_view.html", context)