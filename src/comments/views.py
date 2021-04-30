from django.shortcuts import render, redirect
from .models import Comment
from posts.models import Post

# Create your views here.
def comment_add_view(request, pk):
    # Checking if the current request is post (meaning whether the form was submitted)
    if request.POST:
        try:
            # Getting the comment that was submitted in the get method
            content = request.POST.get('comment')

            # Getting the post for which the comment was submitted (passed in the url)
            post = Post.objects.get(id=pk)

            # Creating a comment for the post and saving it
            comment = Comment(post=post, comment=content, account=request.user)
            comment.save()
        except Exception as e:
            print(e)
    # Going to the main blog site
    return redirect('/blog')
