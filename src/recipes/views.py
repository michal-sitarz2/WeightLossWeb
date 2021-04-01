from django.shortcuts import render
from django.http import HttpResponse

import spoonacular as sp
import requests

def spoonacular_api_view(request):
    api = sp.API("64dadb7cfd724991b7ea9987c4685790")

    jokes_generator = api.get_a_random_food_joke()
    data_jokes = jokes_generator.json()

    recipes_generator = api.get_random_recipes()
    data_recipes = recipes_generator.json()

    return render(request, "spoonacular_api.html", {
        'joke': data_jokes['text'],
        'recipes': data_recipes
    })

