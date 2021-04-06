from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PreferencesForm
from .models import Diet
import requests

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

    # exclude_cuisines = request.session['preferences']['exclude_cuisines']
    # diet = request.session['preferences']['diet']
    # intolerance = request.session['preferences']['intolerance']
    # exclude_ingredients = request.session['preferences']['exclude_ingredients']

    user = request.user.diet
    exclude_cuisines = user.exclude_cuisines
    diet = user.diets
    intolerance = user.intolerances
    exclude_ingredients = user.exclude_ingredients

    url = "https://api.spoonacular.com/recipes/complexSearch"
    querystring = {'excludeCuisine': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                   'excludeIngredients': exclude_ingredients, 'addRecipeNutrition': False, 'number': 7, 'apiKey': 'db078d8202d840b78592794720def365'}
    response = requests.request("GET", url, params=querystring)
    context['response'] = response

    return render(request, "diets/view_recipe_preferences.html", context)