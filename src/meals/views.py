from django.shortcuts import render, redirect
import requests, json

def choose_meals_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")

    context = {}

    '''
    Firstly, the view in diets which allows to view recipes was just for testing,
    hence it will be removed.
    The thing that is currently missing is adding additional filters here.
    We need to sort by the required calories and nutrients for the user, and we also
    need to add a filter for meal_type (which means that we might need to make a couple of
    calls to the API per person just to get breakfast, lunch, dinner and snacks.
    Need to add some way of adding the meals for the user (whether it is manual or 
    automatic; could potentially make it automatic but allow the user to switch a recipe
    if they don't like it).
    '''


    # Information the user has specified for preferences with their recipes
    user = request.user.diet
    exclude_cuisines = user.exclude_cuisines
    diet = user.diets
    intolerance = user.intolerances
    exclude_ingredients = user.exclude_ingredients

    print(exclude_cuisines, diet, intolerance, exclude_ingredients)

    # # # URL to filter a recipe (number set to 1 at the moment)
    url = "https://api.spoonacular.com/recipes/complexSearch"
    querystring = {'excludeCuisine': exclude_cuisines, 'diet': diet, 'intolerances': intolerance,
                   'excludeIngredients': exclude_ingredients, 'addRecipeNutrition': True, 'number': 20,
                   'apiKey': 'db078d8202d840b78592794720def365'}

    # # Getting the response from the API
    response = requests.request("GET", url, params=querystring)
    #
    # # Converting the information to JSON so that it can be used as a dictionary
    data = json.loads(response.text)



    # ## Useful to use when testing. Uncomment the first one when calling the api for the first time per session.
    # ## And then comment the api calls and comment out the data variable to read from session.
    request.session['recipes'] = data
    #data = request.session['recipes']

    recipes = {}

    for i, recipe in enumerate(data['results']):
        i = str(i)
        recipes[i] = []
        recipes[i].append(recipe['title'])
        recipes[i].append(recipe['id'])
        recipes[i].append(recipe['healthScore'])
        recipes[i].append(recipe['servings'])

        # Calories
        recipes[i].append(str(recipe['nutrition']['nutrients'][0]['amount']) + " " + recipe['nutrition']['nutrients'][0]['unit'])
        # Fats
        recipes[i].append(str(recipe['nutrition']['nutrients'][1]['amount']) + " " + recipe['nutrition']['nutrients'][1]['unit'])
        # Saturated Fats
        recipes[i].append(str(recipe['nutrition']['nutrients'][2]['amount']) + " " + recipe['nutrition']['nutrients'][2]['unit'])
        # Carbs
        recipes[i].append(str(recipe['nutrition']['nutrients'][3]['amount']) + " " + recipe['nutrition']['nutrients'][3]['unit'])
        # Sugar
        recipes[i].append(str(recipe['nutrition']['nutrients'][5]['amount']) + " " + recipe['nutrition']['nutrients'][5]['unit'])
        # Protein
        recipes[i].append(str(recipe['nutrition']['nutrients'][8]['amount']) + " " + recipe['nutrition']['nutrients'][8]['unit'])

        recipes[i].append(recipe['image'])

        ingredient_str = ""
        for ingredient in recipe['nutrition']['ingredients']:
            ingredient_str += "{} ({} {}), ".format(ingredient['name'], str(ingredient['amount']), ingredient['unit'])

        ingredient_str = ingredient_str[:-2].capitalize()

        recipes[i].append(ingredient_str)

    context['recipes'] = recipes

    return render(request, "meals/list_recipes.html", context)




