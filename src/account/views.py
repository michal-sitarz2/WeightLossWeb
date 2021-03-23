from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            weight = form.cleaned_data.get('weight')
            height = form.cleaned_data.get('height')
            weight_goal = form.cleaned_data.get('weight_goal')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password, weight=weight, height=height,
                                   weight_goal=weight_goal)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)