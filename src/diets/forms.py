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
    diet = forms.CharField(required=False, help_text="Comma-Separated List of Intolerances (Gluten Free, Ketogenic, Vegetarian, "
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

        # For each of the inputs getting the list, by separating inputs with commas
        exclude_cuisines = self.separate_by_commas(exclude_cuisines)
        diet = self.separate_by_commas(diet)
        intolerance = self.separate_by_commas(intolerance)

        # List of available cuisines (provided by the Spoonacular API)
        available_cuisines = ['african', 'american', 'british', 'cajun', 'caribbean', 'chinese', 'eastern european',
                              'european', 'french', 'german', 'greek', 'indian', 'irish', 'italian', 'japanese',
                              'jewish', 'korean', 'latin american', 'mediterranean', 'mexican', 'middle eastern',
                              'nordic', 'southern', 'spanish', 'thai', 'vietnamese']

        # Checking that all the inputs given are in the available cuisines
        for cuisine in exclude_cuisines:
            # If it is not we stop iterating, and add an error to the exclcude cuisines field
            if cuisine not in available_cuisines:
                self.add_error('exclude_cuisines', 'Please check if values match with the provided values.')
                break

        # List of available diets (provided by the Spoonacular API)
        available_diets = ['gluten free', 'ketogenic', 'vegetarian', 'lacto-vegeterian', 'vegan',
                           'ovo-vegetarian', 'pescetarian', 'paleo', 'primal', 'whole30']

        # Checking that all the inputs given are in the available diets
        for d in diet:
            # If it is not we stop iterating, and add an error to the diets field
            if d not in available_diets:
                self.add_error('diet', 'Please check if values match with the provided values.')
                break

        # List of available intolerances (provided by the Spoonacular API)
        available_intolerances = ['dairy', 'egg', 'gluten', 'grain', 'peanut', 'seafood', 'sesame', 'shellfish',
                                  'soy', 'sulfite', 'tree nut', 'wheat']

        # Checking that all the inputs given are in the available intolerances
        for i in intolerance:
            if i not in available_intolerances:
                # If it is not we stop iterating, and add an error to the intolerances field
                self.add_error('intolerance', 'Please check if values match with the provided values.')
                break

        return data

    # Helper method which returns a list split on the commas
    def separate_by_commas(self, data):
        values = []
        # Checking that the length is not zero
        if len(data) != 0:
            # Splitting the values by comma only if there is a comma
            if ',' in data:
               values = data.lower().split(",")

            else:
                values.append(data.lower())
        # Iterating through all of the values
        for i in range(len(values)):
            # Stripping white spaces at the start
            values[i] = values[i].strip()

        return values