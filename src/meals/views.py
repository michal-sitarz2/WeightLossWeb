from django.shortcuts import render, redirect
from .models import Meal
from collections import OrderedDict

def choose_meals_view(request, pk):
    if not request.user.is_authenticated:
        return redirect("/")

    context = {}

    meals = Meal.objects.order_by('meal_date').filter(diet=request.user.diet)

    breakfast = []
    lunch = []
    dinner = []
    snack = []

    for i, meal in enumerate(meals):
        if i%4==0:
            breakfast.append(meal)
        if i%4==1:
            lunch.append(meal)
        if i%4==2:
            dinner.append(meal)
        if i%4==3:
            snack.append(meal)

    days = {}

    for i in range(len(breakfast)):
        days[breakfast[i].meal_date] = []
        days[breakfast[i].meal_date].append(breakfast[i])
        days[breakfast[i].meal_date].append(lunch[i])
        days[breakfast[i].meal_date].append(snack[i])
        days[breakfast[i].meal_date].append(dinner[i])

    context['days'] = days


    return render(request, "meals/list_recipes.html", context)



