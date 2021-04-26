from django import forms
from .models import Progress

class InitialProgressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # override __init__ to make your "self" object have the instance of the current user
        self.account = kwargs.pop('user', None)
        super(InitialProgressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Progress
        fields = ('starting_weight', 'starting_height', 'target_bmi')
        help_texts = {
            'starting_weight': ('(Kg)'),
            'starting_height': ('(meters)'),
        }

    def save(self, commit=True):
        progress = Progress()
        progress.user = self.account
        progress.starting_weight = self.cleaned_data.get('starting_weight')
        progress.starting_height = self.cleaned_data.get('starting_height')
        progress.target_bmi = self.cleaned_data.get('target_bmi')

        progress.initial_current_set()
        progress.save()

        return progress