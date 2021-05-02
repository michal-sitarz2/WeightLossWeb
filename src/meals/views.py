from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Meal
from recipes.models import Recipe
from collections import OrderedDict
from datetime import datetime, timedelta

from collections import OrderedDict


# Method used to delete meal from the database and make a new meal with the same recipe in two weeks
def delete_meal(request, recipe_id, day, month, year, completed=True):
    # Recomposing the date with the components passed in the url
    # Used because there can be more than one recipe with the same date
    date = datetime(day=day, month=month, year=year)

    # Using try-catch block to check if valid '...(remaining elements truncated)...meals are being deleted
    try:
        # Filtering all the meals with the id, and then getting the one selected based on the date
        meal = Meal.objects.filter(diet=request.user.diet).filter(recipe=recipe_id).get(meal_date=date.date())

        # Deleting the meal from the database
        meal.delete()

        # After deleting the meal, calling a method that will check how many recipes the user has for the given day
        check_daily_completion(date, request.user)

        save_next_recipe(request.user, recipe_id, date)

    # In case something has been done wrong (e.g. a meal which doesn't exist is attempted to be deleted)
    except Exception as e:
        print(e)
        # Sets an error that will be displayed on the dashboard(saying that the meal was not deleted successfully)
        messages.error(request, "The meal couldn't be checked off.")
        # Redirects the user back to the dashboard
        return redirect('user_dashboard', pk=request.user.pk)
    if (completed):
        # Displaying success message on the template indicating that the meal was successfully deleted
        messages.success(request, "The meal was successfully completed!")
        # Refreshing the page and showing the recipe recommendations
        return redirect('view_recipe_recommendations', pk=request.user.pk)

# A helper method which takes in the date for the user meals and checks if the user has completed all
def check_daily_completion(date, user):
    # Getting the meals based on the user and the date of the meal (that was just completed)
    meals = Meal.objects.filter(diet=user.diet).filter(meal_date=date)

    # If there are zero meals retrieved, it means all the meals have been completed
    if(len(meals) == 0):
        streak = user.progress.streak

        # Incrementing the user streak by one
        user.progress.streak = streak + 1
        user.progress.save()
        print(user)


# A method that will be used to get next recipe based on the one that was deleted
def save_next_recipe(user, recipe_id, date):
    # Getting the current recipe that was being deleted
    recipe = Recipe.objects.filter(id=recipe_id)[0]

    # Getting the meal type of the recipe to be able to filter with it the last recipe in the databasae from that meal type
    recipe_meal = recipe.meal_type

    # Filtering the last recipe from that meal type saved in the database
    last_meal = Meal.objects.filter(diet=user.diet).order_by('meal_date').filter(
        diet=user.diet).filter(
        recipe__meal_type=recipe_meal)

    # Checking if there are more meals other than the one that was just deleted
    if (len(last_meal) != 0):
        # Getting the date from the last meal saved
        last_meal = last_meal[len(last_meal) - 1].meal_date

    # Otherwise setting the date for the next meal to be the day after the deleted meal
    else:
        last_meal = date.date()

    # Calculating the next day we want to save the meal on
    next_date = last_meal + timedelta(days=1)

    # Saving the new meal
    meal = Meal(meal_date=next_date, diet=user.diet, recipe=recipe)
    meal.save()

# View to show recipes recommended for the user
def choose_meals_view(request, pk):
    # Checking if the user is logged in
    if not request.user.is_authenticated:
        # If not, redirect to homepage
        return redirect("/")

    try:
        if(request.user.diet):
            pass
    except:
        # If not, redirect to homepage
        return redirect("set_dietary_preferences", request.user.id)

    context = {}

    # Getting all the meals for the specific user (using diet table), and ordering them by the date
    meals = Meal.objects.order_by('meal_date').filter(diet=request.user.diet)

    # Getting all the meals that were in range from some old date to yesterday
    meals_past = meals.filter(meal_date__range=["2000-01-01", datetime.today().date() - timedelta(days=1)])

    # Checking if the length of those past meals is 0
    if(len(meals_past) != 0):
        print(meals_past)

        # Getting the current user's progress
        account_progress = request.user.progress

        # If there were meals that needed to be deleted, streak will be set to zero again
        account_progress.streak = 0
        account_progress.save()

        # If there are meals, they will be deleted as not completed
        for meal in list(meals_past):
            recipe_id = meal.recipe.id
            date = meal.meal_date

            # Deleting meal here
            meal.delete()
            # Shifting the meals to the end of the meal plan
            save_next_recipe(request.user, recipe_id, date)

        # Adding a message for the user to let them know the old recipes were deleted
        messages.error(request, "The old, not completed recipe(s) were deleted.")



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