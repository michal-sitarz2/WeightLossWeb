from django.shortcuts import render, redirect
from .models import Comment
from posts.models import Post

# Create your views here.
def comment_add_view(request, pk):
    context = {}

    # Checking if the current request is post (meaning whether the form was submitted)
    if request.POST:
        try:
            content = request.POST.get('comment')

            post = Post.objects.get(id=pk)

            comment = Comment(post=post, comment=content, account=request.user)
            comment.save()
        except Exception as e:
            print(e)
    return redirect('/blog')
