from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from progress.models import Progress
import requests
import json

from .scripts.bmi_calculate import calculate_BMI
from .twitter import *
# These are for the contact page
from pages.forms import ContactForm
from django.core.mail import EmailMessage
from django.template.loader import get_template

def homepage_view(request, *args, **kwargs):
    context = {}
    return render(request, "homepage.html", context)

def contact_view(request, *args, **kwargs):
    form_class = ContactForm
    
    # the logic behind the contact form
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            # Recaptcha Validation 
            captcha_token = request.POST.get("g-recaptcha-response")
            cap_url = "https://www.google.com/recaptcha/api/siteverify"
            cap_secret = "6Leg4qoaAAAAAKCpXo-sNiMNdtAQPd1_x0ytDXxo"
            cap_data = {"secret": cap_secret, "response": captcha_token}

            cap_server_response = requests.post(url=cap_url, data=cap_data)
            cap_json = json.loads(cap_server_response.text)
            # End Recaptch Validation

            first_name = request.POST.get(
                'first_name'
            , '')
            last_name = request.POST.get(
                'last_name'
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
            if cap_json['success']:
                email.send()
                messages.success(request, 'Message send successfully - look at your console', extra_tags='alert-success')
                return redirect('contact')
            else:
                messages.error(request, 'Please make sure to tick the captcha box before submitting', extra_tags='alert-danger')
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

    # Getting the range in which the user is
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

# Doesn't stream tweets right now, just fetches them.
def articles_view(request, *args, **kwargs):
    tweets = fetch_tweets('FitBottomedGirl ') # Using one example diet account
    context = {'tweets': tweets}
    return render(request, "articles.html", {'text': 'Hello World'})
