from django import forms

def is_anagram(x, y):
    return sorted(x) == sorted(y)

class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def clean_test_value_email(self):
        data = self.cleaned_data.get('email')

        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if not is_anagram(data, 'listen'):
            raise forms.ValidationError('This is invalid email')
        
        return data