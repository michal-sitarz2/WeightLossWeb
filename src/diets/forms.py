from django import forms
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class PreferencesForm(forms.Form):

    daily_calorie_intake = forms.FloatField(required=True, validators=[MinValueValidator(0)],
                                            help_text='Please provide approximate daily calorie intake')

    exclude_cuisines = forms.CharField(required=False, help_text="Comma-Separated List of cuisines to exclude (African, American, "
                                                 "British, Cajun, Caribbean, Chinese,"
                                                 " Eastern European, European, French, German, Greek, Indian, "
                                                 " Irish, Italian, Japanese, Jewish, Korean, Latin American, "
                                                 " Mediterranean, Mexican, Middle Eastern, Nordic, Southern, "
                                                 " Spanish, Thai, Vietnamese)")
    diet = forms.CharField(required=False, help_text="Comma-Separated List of Intolerances (Gluten Free, Ketogenic, Vegeterian, "
                                     "Lacto-vegetarian, Vegan, Ovo-vegetarian, Pescetarian, Paleo, Primal, Whole30)")
    intolerance = forms.CharField(required=False, help_text= "Comma-Separated List of Intolerances (Dairy, Egg, Gluten, Grain, Peanut, "
                                             " Seafood, Sesame, Shellfish, Soy, Sulfite, Tree Nut, Wheat)")
    exclude_ingredients = forms.CharField(required=False, help_text="Comma-Separated List of Ingredients to Exclude")

    # Using the clean method to validate whether all of the fields inputted are matching the available ones
    def clean(self):
        data = self.cleaned_data
        exclude_cuisines = data["exclude_cuisines"]
        diet = data['diet']
        intolerance = data['intolerance']

        exclude_cuisines = self.separate_by_commas(exclude_cuisines)
        diet = self.separate_by_commas(diet)
        intolerance = self.separate_by_commas(intolerance)

        available_cuisines = ['african', 'american', 'british', 'cajun', 'caribbean', 'chinese', 'eastern european',
                              'european', 'french', 'german', 'greek', 'indian', 'irish', 'italian', 'japanese',
                              'jewish', 'korean', 'latin american', 'mediterranean', 'mexican', 'middle eastern',
                              'nordic', 'southern', 'spanish', 'thai', 'vietnamese']

        for cuisine in exclude_cuisines:
            if cuisine not in available_cuisines:
                self.add_error('exclude_cuisines', 'Please check if values match with the provided values.')
                break

        available_diets = ['gluten free', 'ketogenic', 'vegeterian', 'lacto-vegeterian', 'vegan',
                           'ovo-vegetarian', 'pescetarian', 'paleo', 'primal', 'whole30']
        for d in diet:
            if d not in available_diets:
                self.add_error('diet', 'Please check if values match with the provided values.')
                break

        available_intolerances = ['dairy', 'egg', 'gluten', 'grain', 'peanut', 'seafood', 'sesame', 'shellfish',
                                  'soy', 'sulfite', 'tree nut', 'wheat']

        for i in intolerance:
            if i not in available_intolerances:
                self.add_error('intolerance', 'Please check if values match with the provided values.')
                break

        return data


    def separate_by_commas(self, data):
        values = []
        if len(data) != 0:
            if ',' in data:
               values = data.lower().split(",")
            else:
                values.append(data.lower())

        for i in range(len(values)):
            values[i] = values[i].strip()

        return values