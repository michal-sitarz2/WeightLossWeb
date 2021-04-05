from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from .forms import RegistrationForm, AccountAuthenticationForm
from .models import Account


def dashboard_view(request, pk):
    context = {}
    try:
        if request.user.progress:
            return render(request, 'account/dashboard.html', context)
    except Exception as e:
        return redirect('progress_form')

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, email=email, password=raw_password)
            login(request, account)

            return redirect('progress_form')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_admin:
            return redirect('/admin')
        else:
            return redirect('user_dashboard', user.pk)

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                if user.is_admin:
                    return redirect('/admin')
                else:
                    return redirect('user_dashboard', user.pk)
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)
