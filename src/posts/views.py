from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostsForm
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from comments.models import Comment


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/blog_update_post.html'
    fields = ['title', 'content', 'anonimity']

    def form_valid(self, form):
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        anonimity = form.cleaned_data["anonimity"]

        post = self.object
        post.title = title
        post.content = content
        post.anonimity = anonimity
        post.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/blog/userPosts"


def blog_delete_post(request, pk):
    try:
        post = Post.objects.filter(user=request.user).get(id=pk)
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
    posts = Post.objects.all().order_by('-date').filter(user=request.user)

    post_map = {}

    for post in posts:
        post_map[post] = []
        comments = Comment.objects.filter(post=post).order_by('date')
        for comment in comments:
            post_map[post].append(comment)

    context['posts'] = post_map

    return render(request, "posts/blog_post_user.html", context)

def blog_post_view(request):
    if(not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    context = {}

    posts = Post.objects.all().order_by('-date').filter(~Q(user=request.user))

    post_map = {}

    for post in posts:
        post_map[post] = []
        comments = Comment.objects.filter(post=post).order_by('date')
        for comment in comments:
            post_map[post].append(comment)

    context['posts'] = post_map

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
            return redirect('/blog/userPosts')
        else:
            context['posts_form'] = form

    else:
        form = PostsForm(request.POST, user=user)
        context['posts_form'] = form

    return render(request, 'posts/blog_make_post.html', context)
