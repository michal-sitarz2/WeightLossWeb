from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from .forms import RegistrationForm, AccountAuthenticationForm
from pages.scripts.bmi_calculate import calculate_BMI
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from account.models import Account

# Dashboard view
def dashboard_view(request, pk):
    context = {}

    try:
        if(request.user.progress):
            pass
    except:
        return redirect("/registration_progress")
    #registration_progress

    # Getting the progress for the current user
    user_progress = request.user.progress
    # From the progress, getting what the target bmi is for the user
    target = user_progress.target_bmi
    # From the progress, getting what the current bmi is for the user
    current = user_progress.current_bmi
    # With current and target bmi calculating what the starting bmi was
    starting = calculate_BMI(user_progress.starting_weight, user_progress.starting_height)

    # Putting the progress in range between the starting and the target bmi
    # Getting the percentage by dividing the differences starting-current with starting-target
    progress_width = (((starting - current)/(starting - target) * 100))

    # Getting the reverse of the progress, in order to get the length of the bar going towards zero
    progress = (100 - ((starting - current)/(starting - target) * 100))

    # Putting the progress in range in case the current bmi is higher than starting, or smaller than target
    if(progress <= 0):
        progress = 0
        progress_width = 100
    if(progress >= 100):
        progress = 100
        progress_width = 0

    context['progress_width'] = int(progress_width)
    context['progress_percentage'] = int(progress)

    # Returning the dashboard if the user was registered and progress was created for them
    # (i.e. the progress form was filled)
    try:
        if request.user.progress:
            return render(request, 'account/dashboard.html', context)
    # Otherwise they will be taken to the progress form to complete the registration
    except Exception as e:
        return redirect('progress_form')

# Registration form for the user
def registration_view(request):
    context = {}

    # Checking if the current request is post (meaning whether the form was submitted)
    if request.POST:
        # getting the registration form
        form = RegistrationForm(request.POST)
        # Checking if all of the inputs to the form are valid
        if form.is_valid():
            # Saving the form
            form.save()
            # Getting the data from the form
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # Authenticating the user with the username, email and password
            account = authenticate(username=username, email=email, password=raw_password)
            # Logging the user in if everything is authenticated
            login(request, account)

            messages.success(request, 'Well done, you have created your account. Please fill in this form to get you started.',
                             extra_tags='alert-success')
            # Once the user is logged in they are taken to the progress form to fill in the rest of data required
            return redirect('progress_form')
        else:
            # If the form was not valid, it will be displayed back
            context['registration_form'] = form
            # Getting the errors from the form
            context['form_errors'] = []
            for fields in form:
                if fields.errors:
                    context['form_errors'].append(fields.errors)
    else:
        # If it was not submitted (hence it was GET) the form will be displayed for the user to fill in
        form = RegistrationForm()
        context['registration_form'] = form
    # Rendering the template with the registration form which is passed in the dictionary 'context'
    return render(request, 'account/register.html', context)

# Function for the user to log out of the website
def logout_view(request):
    # Logging the user out
    logout(request)
    # Once user is logged out taking them back to the home page
    return redirect('home')

# Login view for the user to login into the website
def login_view(request):
    context = {}
    # Getting the current user
    user = request.user
    # Checking whether the user is logged in/authenticated
    if user.is_authenticated:
        if user.is_admin:
        # If the user is authenticated and the user is an admin, they are taken to the admin page
            return redirect('/admin')
        else:
            # However, if the user is logged in and they are not the admin, they are taken to the dashboard
            return redirect('user_dashboard', user.pk)

    # If the user is not authenticated, checking whether the request was post or get
    if request.POST:
        # If it was post, it means the form was submitted, and hence retrieving it
        form = AccountAuthenticationForm(request.POST)
        # Checking if the form is valid
        if form.is_valid():
            # If valid, getting the inputs
            username = request.POST['username']
            password = request.POST['password']
            # Authenticating the user based on the username and password
            user = authenticate(username=username, password=password)

            if user:
                # If the user is authenticated logging them in
                login(request, user)
                if user.is_admin:
                    return redirect('/admin')
                else:
                    return redirect('user_dashboard', user.pk)
        else:
            # Getting the errors from the form
            context['form_errors'] = []
            for fields in form:
                if fields.errors:
                    context['form_errors'].append(fields.errors)
    # If the request is GET display the form
    else:
        form = AccountAuthenticationForm()

    # Sending the form if the user was not redirected
    context['login_form'] = form
    return render(request, 'account/login.html', context)


# Method which deletes the user account
def user_delete(request, user):
    # Checking if the user confirmed
    if request.POST:
        # Checking if the user is deleting their own account
        if request.user.pk == user:
            try:
                # Trying to get the user
                delete_user = Account.objects.get(pk=request.user.pk)
                # Deleting the user
                delete_user.delete()
            except Exception as e:
                pass

            # Adding a message which will ensure the user that the account was deleted
            messages.success(request, 'Your account was permanently deleted, along with all of your data. ',
                             extra_tags='alert-success')

            # Redirecting the user to the home page
            return redirect("/")
        else:
            # If the user is trying to delete someone elses account, they will be redirected back to the
            # Dashboard
            messages.error(request, 'This account cannot be deleted!')
            return redirect('/account/dashboard/{}'.format(request.user.pk))
    # Returning the page with the confirmation form if the GET request is ade
    return render(request, "account/account_confirm_delete.html", {})