from django import forms

class SearchRecipeForm(forms.Form):
    # This is for a search input to look through the API 

    search_query = forms.CharField(help_text="Search something like: Chicken with rice")




