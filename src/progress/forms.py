from django import forms
from .models import Progress
from django.http import HttpResponse, HttpResponseRedirect

from pages.scripts.bmi_calculate import calculate_BMI

# Generic Update view for the Progress class
class SetNewGoal(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # override __init__ to make your "self" object have the instance of the current user
        self.account = kwargs.pop('user', None)
        super(SetNewGoal, self).__init__(*args, **kwargs)

        self.fields['current_weight'].widget.attrs['value'] = self.account.progress.current_weight
        self.fields['current_height'].widget.attrs['value'] = self.account.progress.current_height
        self.fields['target_bmi'].widget.attrs['value'] = self.account.progress.target_bmi

    class Meta:
        # Defining the model for which the update view is for
        model = Progress
        # Name of the template to use
        template_name = 'progress/progress_edit.html'
        # Fields that we want to edit (we don't want to edit the goal).
        fields = ['current_weight', 'current_height', 'target_bmi']

    # Method to check if the data inputted is correct
    # Mainly applies to the target BMI, which has to be smaller than the current BMI
    def clean(self):
        # Getting the data
        data = self.cleaned_data

        print(data)

        height = data["current_height"]
        weight = data["current_weight"]
        target_bmi = data["target_bmi"]

        # Calculating the current BMI
        current_bmi = calculate_BMI(weight, height)

        # Checking if the target BMI is valid, else adding an error
        if current_bmi <= target_bmi:
            self.add_error('target_bmi', 'Please put a BMI lower than your current one: {}'.format(current_bmi))

        return data

    def save(self):
        # making a progress with the inputs from the form
        starting_weight = self.cleaned_data.get('current_weight')
        starting_height = self.cleaned_data.get('current_height')
        target_bmi = self.cleaned_data.get('target_bmi')



        # Setting the current height, weight and BMI to be equal to starting
        self.account.progress.update_current_set(starting_height, starting_weight, target_bmi=target_bmi)

        self.account.progress.save()

        return self.account



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

    # Method to check if the data inputted is correct
    # Mainly applies to the target BMI, which has to be smaller than the current BMI
    def clean(self):
        # Getting the data
        data = self.cleaned_data

        target_bmi = data["target_bmi"]
        starting_height = data["starting_height"]
        starting_weight = data["starting_weight"]

        # Calculating the current BMI
        current_bmi = calculate_BMI(starting_weight, starting_height)

        # Checking if the target BMI is valid, else adding an error
        if current_bmi <= target_bmi:
            self.add_error('target_bmi', 'Please put a BMI lower than your current one: {}'.format(current_bmi))

        return data

    # Overwritting the save method as we need to also set the initial values with helper method
    def save(self, commit=True):
        # making a progress with the inputs from the form
        progress = Progress()
        progress.user = self.account
        progress.starting_weight = self.cleaned_data.get('starting_weight')
        progress.starting_height = self.cleaned_data.get('starting_height')
        progress.target_bmi = self.cleaned_data.get('target_bmi')

        # Setting the current height, weight and BMI to be equal to starting
        progress.initial_current_set()
        progress.save()

        return progress