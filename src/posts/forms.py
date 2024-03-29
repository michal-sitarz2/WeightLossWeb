from django.forms import ModelForm, forms
from .models import Post

class PostsForm(ModelForm):
    # Creating a new init method as we want to pass a user which will be set
    def __init__(self, *args, **kwargs):
        # override __init__ to make your "self" object have the instance of the current user
        self.account = kwargs.pop('user', None)
        super(PostsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'content', 'anonimity']

    # Function saving the post corresponding to the current user
    def save(self, commit=True):
        posts = Post()
        posts.user = self.account
        posts.content = self.cleaned_data.get('content')
        posts.title = self.cleaned_data.get('title')

        posts.anonimity = self.cleaned_data.get('anonimity')
        posts.save()

        return posts


