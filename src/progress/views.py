from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import InitialProgressForm, SetNewGoal
from django.views.generic import UpdateView
from .models import Progress



# View showing the progress form
def progress_form_edit(request, pk):
    context = {}
    # Getting the current user
    user = request.user

    if not user.is_authenticated:
        return redirect('home')

    # Displaying the form if the request is post
    if request.POST:
        form = SetNewGoal(request.POST, user=user)

        # Checking if the form is valid
        if (form.is_valid()):
            # Saving the data from the form
            form.save()
            return redirect('user_dashboard', user.pk)
        else:
            context['form'] = form

            context['form_errors'] = []
            for fields in form:
                if fields.errors:
                    context['form_errors'].append(fields.errors)

    else:
        # Displaying the form on the page with the current user
        form = SetNewGoal(user=user)
        context['form'] = form

    return render(request, 'progress/progress_edit.html', context)

# View showing the progress form
def progress_form_view(request):
    context = {}
    # Getting the current user
    user = request.user

    # If the user is not logged in take them to log in
    if not request.user.is_authenticated:
        return redirect('login')

    # Checking if user already has progress, if they do, they will be redirected
    try:
        if user.progress:
            return redirect('home')
    except Exception:
        # Displaying the form if the request is post
        if request.POST:
            form = InitialProgressForm(request.POST, user=user)

            # Checking if the form is valid
            if (form.is_valid()):
                # Saving the data from the form
                form.save()
                return redirect('user_dashboard', user.pk)
            else:
                context['progress_form'] = form

                context['form_errors'] = []
                for fields in form:
                    if fields.errors:
                        context['form_errors'].append(fields.errors)

        else:
            # Displaying the form on the page with the current user
            form = InitialProgressForm(user=user)
            context['progress_form'] = form

    return render(request, 'progress/progress_form.html', context)

# Generic Update view for the Progress class
class UpdateProgressView(UpdateView):
    # Defining the model for which the update view is for
    model = Progress
    # Name of the template to use
    template_name = 'progress/progress_edit.html'
    # Fields that we want to edit (we don't want to edit the goal).
    fields = ['current_weight', 'current_height']

    # Validating the form
    def form_valid(self, form):
        # Getting the data from the form
        weight = form.cleaned_data["current_weight"]
        height = form.cleaned_data["current_height"]


        # Calling a helper function from the progress model which updates the current progress
        self.object.update_current_set(height, weight)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # Link to where the user gets redirected to
    def get_success_url(self):
        return "/account/dashboard/{}".format(self.object.user.pk)



