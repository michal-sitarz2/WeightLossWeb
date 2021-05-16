from django import forms
from .models import Progress

from pages.scripts.bmi_calculate import calculate_BMI

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

    def clean(self):
        data = self.cleaned_data

        target_bmi = data["target_bmi"]
        starting_height = data["starting_height"]
        starting_weight = data["starting_weight"]

        current_bmi = calculate_BMI(starting_weight, starting_height)

        if current_bmi <= target_bmi:
            self.add_error('target_bmi', 'Please put a BMI lower than your current one: {}'.format(current_bmi))

        return data


    def save(self, commit=True):
        progress = Progress()
        progress.user = self.account
        progress.starting_weight = self.cleaned_data.get('starting_weight')
        progress.starting_height = self.cleaned_data.get('starting_height')
        progress.target_bmi = self.cleaned_data.get('target_bmi')

        progress.initial_current_set()
        progress.save()

        return progress