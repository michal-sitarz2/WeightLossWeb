from django.http import HttpResponse
from django.shortcuts import render

from .scripts.bmi_calculate import calculate_BMI


def homepage_view(request, *args, **kwargs):
    return render(request, "homepage.html", {})


def bmi_calculator_view(request, *args, **kwargs):
    # Creating a dictionary to pass to the HTML view
    # Setting initial value to -2, which will indicate that a value for BMI is still required
    bmi = {'bmi': -2}
    BMI = 0

    # Using try and except block in case GET is empty or if it doesn't have 'weight' or 'height' variables
    try:
        # Getting the weight and height variables for Metric system
        weight = float(request.GET['weight_metric'])
        height = float(request.GET['height_metric'])

        bmi['weight_metric'] = weight
        bmi['height_metric'] = height

        # Calling a function to calculate BMI and saving it into the dictionary
        # If the value for BMI will be -1, it means that an error has occurred
        BMI = calculate_BMI(weight, height)
        bmi['bmi'] = BMI

    # If there are errors caught, nothing happens; i.e. the website won't display BMI, because no weight and height
    # were given
    except KeyError:
        pass
    except ValueError:
        pass

    _range = ""
    if BMI != 0:
        if BMI < 18.5:
            _range = "Underweight"
        elif 18.5 <= BMI < 25:
            _range = "Healthy Weight"
        elif 25 <= BMI < 30:
            _range = "Overweight"
        elif 30 <= BMI < 40:
            _range = "Obese"
        else:
            _range = "Extremely Obese"

        bmi['range'] = _range

    return render(request, "bmi_calculator.html", bmi)
