from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import InitialProgressForm
from django.views.generic import UpdateView
from .models import Progress

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
                return redirect('user_dashboard', user.pk)
            else:
                context['progress_form'] = form

        else:
            form = InitialProgressForm(request.POST, user=user)
            context['progress_form'] = form

    return render(request, 'progress/progress_form.html', context)

class UpdateProgressView(UpdateView):
    model = Progress
    template_name = 'progress/progress_edit.html'
    fields = ['current_weight', 'current_height']

    def form_valid(self, form):
        weight = form.cleaned_data["current_weight"]
        height = form.cleaned_data["current_height"]

        self.object.update_current_set(height, weight)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/account/dashboard/{}".format(self.object.user.pk)



