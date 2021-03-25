from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InitialProgressForm


def progress_form_view(request):
    context = {}
    user = request.user

    if not request.user.is_authenticated:
        return redirect('login')

    # Checking if user already has progress, if they do, they will be redirected
    try:
        if user.progress:
            return redirect('home')
    except Exception:
        if request.POST:
            form = InitialProgressForm(request.POST, user=user)

            if (form.is_valid()):
                form.save()

### REDIRECT TO DASHBOARD
                return redirect('home')
            else:
                context['progress_form'] = form

        else:
            form = InitialProgressForm(request.POST, user=user)
            context['progress_form'] = form

    return render(request, 'progress/progress_form.html', context)


