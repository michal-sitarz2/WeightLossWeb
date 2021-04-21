from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Meal
from recipes.models import Recipe
from collections import OrderedDict
from datetime import datetime, timedelta

from collections import OrderedDict


# Method used to delete meal from the database and make a new meal with the same recipe in two weeks
def delete_meal(request, recipe_id, day, month, year):
    # Recomposing the date with the components passed in the url
    # Used because there can be more than one recipe with the same date
    date = datetime(day=day, month=month, year=year)

    # Using try-catch block to check if valid meals are being deleted
    try:
        # Filtering all the meals with the id, and then getting the one selected based on the date
        meal = Meal.objects.filter(diet=request.user.diet).filter(recipe=recipe_id).get(meal_date=date.date())

        # Deleting the meal from the database
        meal.delete()

        # Getting the current recipe that was being deleted
        recipe = Recipe.objects.filter(id=recipe_id)[0]

        # Getting the meal type of the recipe to be able to filter with it the last recipe in the databasae from that meal type
        recipe_meal = recipe.meal_type

        # Filtering the last recipe from that meal type saved in the database
        last_meal = Meal.objects.filter(diet=request.user.diet).order_by('meal_date').filter(diet=request.user.diet).filter(
            recipe__meal_type=recipe_meal)

        # Checking if there are more meals other than the one that was just deleted
        if(len(last_meal) != 0):
            # Getting the date from the last meal saved
            last_meal = last_meal[len(last_meal) - 1].meal_date
        # Otherwise setting the date for the next meal to be the day after the deleted meal
        else:
            last_meal = date.date()

        # Calculating the next day we want to save the meal on
        next_date = last_meal + timedelta(days=1)

        # Saving the new meal
        meal = Meal(meal_date=next_date, diet=request.user.diet, recipe=recipe)
        meal.save()

    # In case something has been done wrong (e.g. a meal which doesn't exist is attempted to be deleted)
    except Exception as e:
        print(e)
        # Sets an error that will be displayed on the dashboard(saying that the meal was not deleted successfully)
        messages.error(request, "The meal couldn't be checked off.")
        # Redirects the user back to the dashboard
        return redirect('user_dashboard', pk=request.user.pk)

    # Displaying success message on the template indicating that the meal was successfully deleted
    messages.success(request, "The meal was successfully completed!")
    # Refreshing the page and showing the recipe recommendations
    return redirect('view_recipe_recommendations', pk=request.user.pk)

# View to show recipes recommended for the user
def choose_meals_view(request, pk):
    # Checking if the user is logged in
    if not request.user.is_authenticated:
        # If not, redirect to homepage
        return redirect("/")

    context = {}

    # Getting all the meals for the specific user (using diet table), and ordering them by the date
    meals = Meal.objects.order_by('meal_date').filter(diet=request.user.diet)

    # Defining dictionaries for each meal type
    breakfast = {}
    lunch = {}
    dinner = {}
    snack = {}

    # Sorting the meals into their respecitve dictionaries based on meal type
    for meal in meals:
        i = meal.meal_date
        if meal.recipe.meal_type.lower() == "breakfast":
            breakfast[i] = meal
        if meal.recipe.meal_type.lower() == "lunch":
            lunch[i] = meal
        if meal.recipe.meal_type.lower() == "dinner":
            dinner[i] = meal
        if meal.recipe.meal_type.lower() == "snack":
            snack[i] = meal

    # Defining days dictionary which will use date as a key, and values will be arrays of meals for that day
    days = {}

    # Calling fill_days method to fill in the meals for each meal on each day
    days = fill_days(days, breakfast)
    days = fill_days(days, lunch)
    days = fill_days(days, dinner)
    days = fill_days(days, snack)

    # Sorting the array by the keys (hence by the dates)
    days = OrderedDict(sorted(days.items()))

    # Saving the days into the context dictionary, which will be passed to the template
    context['days'] = days

    # Returning the template with all the recipes for each specific day
    return render(request, "meals/list_recipes.html", context)

# Method to sort recipes by day and meal
def fill_days(days, dict):
    # Loops through all the meals and dates
    for date, meal in dict.items():
        # Trying to save the meal into the array
        try:
            days[date].append(meal)
        # If there doesn't exist a date in the days array (to append the meal to), then KeyError will be catched
        except KeyError:
            # If this exception happens a list is created
            days[date] = []
            # The meal is added to that specific day
            days[date].append(meal)

    # Returning the filled in dictionary of days for a specific meal
    return days