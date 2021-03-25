from django import forms
from django.contrib.auth import authenticate

from .models import Progress
from account.models import Account

class InitialProgressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # override __init__ to make your "self" object have the instance of the current user
        self.account = kwargs.pop('user', None)
        super(InitialProgressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Progress
        fields = ('starting_weight', 'starting_height', 'target_bmi')

    def save(self, commit=True):
        progress = Progress()
        progress.user = self.account
        progress.starting_weight = self.cleaned_data.get('starting_weight')
        progress.starting_height = self.cleaned_data.get('starting_height')
        progress.target_bmi  = self.cleaned_data.get('target_bmi')

        progress.initial_current_set()
        progress.save()

        return progress






#### Form for updating the Progress (i.e. setting new weight...)