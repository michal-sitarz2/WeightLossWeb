from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post
from .forms import PostsForm
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from comments.models import Comment

# Class which uses generic update view for the class
class UpdatePostView(UpdateView):
    # Defining that the model we want the update view for is the Posts
    model = Post
    # The template we want to use for the Update view
    template_name = 'posts/blog_update_post.html'
    # Fields we want to allow the user to change
    fields = ['title', 'content', 'anonimity']

    # Function checking if the form is valid
    def form_valid(self, form):
        # Getting all the data
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        anonimity = form.cleaned_data["anonimity"]

        # Updating the post with the new data from the form
        post = self.object
        post.title = title
        post.content = content
        post.anonimity = anonimity
        # Saving the form
        post.save()
        return HttpResponseRedirect(self.get_success_url())

    # Success url is the url we want to take the user to after completing the form
    def get_success_url(self):
        return "/blog/userPosts"

# Function which is used to delete the post
def blog_delete_post(request, pk):
    # Trying to get the post by the user, with the post id passed through the url
    try:
        post = Post.objects.filter(user=request.user).get(id=pk)
        # Deleting the Post
        post.delete()
    # Catching exception if the user tries to delete a post that does not exists and then redirect them to the blog page
    except Exception as e:
        messages.error(request, 'Please delete a valid post')
        return redirect('/blog')
    # Taking the user to their posts, as that is where they will be deleting their posts
    return redirect('/blog/userPosts/')

# View which shows current user's posts
def blog_post_view_user(request):
    # If the user is not logged in, they will be taken to the home page with an error message
    if (not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    context = {}
    # Getting all the posts, and ordering them by the newest date, and filter ones by the current user
    posts = Post.objects.all().order_by('-date').filter(user=request.user)

    # Calling the helper function to assign all comments to posts
    context['posts'] = assign_comments_to_posts(posts)

    # Returning the template with all the current user's posts
    return render(request, "posts/blog_post_user.html", context)

# Helper function assigning comments to their corresponding posts
def assign_comments_to_posts(posts):
    post_map = {}

    # Iterating through the posts
    for post in posts:
        # Saving the post to the map as the key and initializing an empty array where comments will be added
        post_map[post] = []
        # Getting all the comments belonging to the current post, and ordering them by the date (form oldest to newest)
        comments = Comment.objects.filter(post=post).order_by('date')
        # Iterating through those comments
        for comment in comments:
            # Adding those comments to the list which is a the value of the post
            post_map[post].append(comment)

    return post_map


# View which shows all the other users posts
def blog_post_view(request):
    # If the user is not logged in, they will be taken to the home page with an error message
    if(not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    context = {}

    # Getting all the posts, and ordering them by the newest date, and filtering those that do not belong to the current user
    posts = Post.objects.all().order_by('-date').filter(~Q(user=request.user))

    # Calling the helper function to assign all comments to posts
    context['posts'] = assign_comments_to_posts(posts)

    return render(request, "posts/blog_post.html", context)


# View to add a new blog post
def blog_post_add(request):
    # If the user is not logged in, take them back to the home page with the error message.
    if (not request.user.is_authenticated):
        messages.error(request, 'Please log in to access the Blog')
        return redirect('/')

    # Getting the current user from the request
    user = request.user
    context = {}

    # If the request was post it means the form was submitted
    if request.POST:
        # Getting the form
        form = PostsForm(request.POST, user=user)
        # Checking if the form was valid
        if (form.is_valid()):
            # Saving the form
            form.save()
            # Taking the user to their posts
            return redirect('/blog/userPosts')
        # If the form was not valid set the form
        else:
            context['posts_form'] = form
    # If GET request, display the form
    else:
        # pass on the user along with the request to the form, as the user will be pre-defined (no need to fill it in)
        form = PostsForm(request.POST, user=user)
        context['posts_form'] = form

    return render(request, 'posts/blog_make_post.html', context)
