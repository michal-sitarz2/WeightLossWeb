from django.http import HttpResponse
from django.shortcuts import render

from .scripts.bmi_calculate import calculate_BMI, calculate_Imperial_BMI

def homepage_view(request, *args, **kwargs):
    return render(request, "homepage.html", {})

def bmi_calculator_view(request, *args, **kwargs):
    # Creating a dictionary to pass to the HTML view
    # Setting initial value to -2, which will indicate that a value for BMI is still required
    bmi = {'bmi': -2}
    # Using try and except block in case GET is empty or if it doesn't have 'weight' or 'height' variables
    try:
        # Getting the weight and height variables
        weight = float(request.GET['weight'])
        height = float(request.GET['height'])

        # Calling a function to calculate BMI and saving it into the dictionary
        # If the value for BMI will be -1, it means that an error has occurred
        bmi['bmi'] = calculate_BMI(weight, height)
    # If there are errors caught, nothing happens; i.e. the website won't display BMI, because no weight and height
    # were given
    except KeyError:
        pass
    return render(request, "bmi_calculator.html", bmi)
