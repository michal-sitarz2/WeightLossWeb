from django import forms

class PreferencesForm(forms.Form):
    '''
    User-set information
    excludeCuisine (comma separated)
    => African, American, British, Cajun, Caribbean, Chinese,
    Eastern European, European, French, German, Greek, Indian,
    Irish, Italian, Japanese, Jewish, Korean, Latin American,
    Mediterranean, Mexican, Middle Eastern, Nordic, Southern,
    Spanish, Thai, Vietnamese

    diet (diet for which the recipes must be suitable) =>
    => gluten free, ketogenic, vegeterian, lacto-vegetarian, vegan, ovo-vegetarian,...
    pescetarian, Paleo, primal, whole30.

    intolerances (comma separated list of intolerances) =>
    dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish,...
    soy, sulfite, tree nut, wheat.

    excludeIngredients (comma-separated list of ingredients or types) e.g. eggs

    Useful Functions
    type (meal type) =>
    main course, side dish, dessert, appetizer, salad, bread, breakfast,...
    soup, beverage, sauce, marinade, fingerfood, snack, drink

    addRecipeNutrition => True

    For filtering: minCarbs, maxCarbs, minProtein, maxProtein, minCalories, maxCalories, minFat, maxFat
    healthScore
    '''

    exclude_cuisines = forms.CharField(help_text="Comma-Separated List of cuisines to exclude (African, American, "
                                                 "British, Cajun, Caribbean, Chinese,"
                                                 " Eastern European, European, French, German, Greek, Indian, "
                                                 " Irish, Italian, Japanese, Jewish, Korean, Latin American, "
                                                 " Mediterranean, Mexican, Middle Eastern, Nordic, Southern, "
                                                 " Spanish, Thai, Vietnamese)")
    diet = forms.CharField(help_text="Comma-Separated List of Intolerances (Gluten Free, Ketogenic, Vegeterian, "
                                     "Lacto-vegetarian, Vegan, Ovo-vegetarian, Pescetarian, Paleo, Primal, Whole30)")
    intolerance = forms.CharField(help_text= "Comma-Separated List of Intolerances (Dairy, Egg, Gluten, Grain, Peanut, "
                                             " Seafood, Sesame, Shellfish, Soy, Sulfite, Tree Nut, Wheat)")
    exclude_ingredients = forms.CharField(help_text="Comma-Separated List of Ingredients to Exclude")

    ### A method to check if the given values are acceptable
    # def clean(self):
    #     data = self.cleaned_data
    #     exclude_cuisines = data["exclude_cuisines"]
    #
    #     # diet = cleaned_data.get("diet")
    #     # intolerance = cleaned_data.get("intolerance")
    #     # exclude_ingredients = cleaned_data.get("exclude_ingredients")
    #
    #     cuisines_arr = []
    #     if len(exclude_cuisines) != 0:
    #         if ',' in exclude_cuisines:
    #             cuisines_arr = exclude_cuisines.lower().split(",")
    #         else:
    #             cuisines_arr.append(exclude_cuisines.lower())

    #     return cuisines_arr


