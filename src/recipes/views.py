from django.shortcuts import render
from django.http import HttpResponse

# import spoonacular as sp
import requests

# def spoonacular_api_view(request):
#     api = sp.API("64dadb7cfd724991b7ea9987c4685790")

#     jokes_generator = api.get_a_random_food_joke()
#     data_jokes = jokes_generator.json()

#     recipes_generator = api.get_random_recipes()
#     data_recipes = recipes_generator.json()

#     return render(request, "spoonacular_api.html", {
#         'joke': data_jokes['text'],
#         'recipes': data_recipes
#     })

def spoonacular_api_search_view(request):
    context = {}

    url = "https://api.spoonacular.com/recipes/complexSearch"

    querystring = {"query": "Chicken with Rice", 'apiKey':'db078d8202d840b78592794720def365'}


    response = requests.request("GET", url, params=querystring)

    context['response'] = response
    return render(request, "recipes/spoonacular_search_view.html", context)