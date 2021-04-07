from django.http import HttpResponse
from django.shortcuts import render, redirect
from progress.models import Progress
import requests

from .scripts.bmi_calculate import calculate_BMI
# These are for the contact page
from pages.forms import ContactForm
from django.core.mail import EmailMessage
from django.template.loader import get_template

# def api_view(request):
#     context = {}
#     querystring = {'q': 'obesity','apiKey': 'a7064ee7edae4d928c4e9e5a8691acc3'}
#     response = requests.request("GET", "https://newsapi.org/v2/everything", params=querystring)
#
#     context['response'] = response
#
#     return render(request,,context)


def homepage_view(request, *args, **kwargs):
    context = {}
    return render(request, "homepage.html", context)

def contact_view(request, *args, **kwargs):
    form_class = ContactForm

    # the logic behind the contact form
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            first_name = request.POST.get(
                'first_name'
            , '')
            last_name = request.POST.get(
                'last_name'
            , '')
            username = request.POST.get(
                'username'
            , '')
            email = request.POST.get(
                'email'
            , '')
            form_message = request.POST.get('message', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'form_message': form_message,
            }
            message = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                message,
                "The Nutritionist" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': email }
            )
            email.send()
            return redirect('contact')

    return render(request, "contact.html", {
        'form': form_class
    })


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
