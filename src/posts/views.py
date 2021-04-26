from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostsForm
from django.db.models import Q

def blog_delete_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
        post.delete()
    except Exception as e:
        messages.error(request, 'Please delete a valid post')
        return redirect('/blog')

    return redirect('/blog/userPosts/')


def blog_post_view_user(request):
    if (not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    context = {}
    context['posts'] = Post.objects.all().order_by('-date').filter(user=request.user)

    return render(request, "posts/blog_post_user.html", context)

def blog_post_view(request):
    if(not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    context = {}
    context['posts'] = Post.objects.all().order_by('-date').filter(~Q(user=request.user))

    return render(request, "posts/blog_post.html", context)



def blog_post_add(request):
    if (not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    user = request.user
    context = {}

    if request.POST:
        form = PostsForm(request.POST, user=user)

        if (form.is_valid()):
            form.save()
            return redirect('blog_post_board')
        else:
            context['posts_form'] = form

    else:
        form = PostsForm(request.POST, user=user)
        context['posts_form'] = form

    return render(request, 'posts/blog_make_post.html', context)
