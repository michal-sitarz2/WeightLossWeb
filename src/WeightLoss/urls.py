"""WeightLoss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import homepage_view, bmi_calculator_view, contact_view
from account.views import registration_view, logout_view, login_view, dashboard_view
from progress.views import progress_form_view, UpdateProgressView
from recipes.views import spoonacular_api_search_view, spoonacular_api_search_form, view_recipe
from diets.views import set_preferences_form
from meals.views import choose_meals_view, delete_meal
from posts.views import blog_post_view, blog_post_add, blog_post_view_user, blog_delete_post, UpdatePostView
from comments.views import comment_add_view

urlpatterns = [
    path('', homepage_view, name="home"),
    path('home/', homepage_view, name="home"),
    path('bmi/', bmi_calculator_view, name="bmi"),
    path('admin/', admin.site.urls),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name='login'),
    path('registration_progress/', progress_form_view, name='progress_form'),
    path('contact/', contact_view, name="contact"),
    path('progress/edit/<int:pk>', UpdateProgressView.as_view(), name="update_progress"),
    path('post/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    path('account/dashboard/<int:pk>', dashboard_view, name='user_dashboard'),
    path('search/', spoonacular_api_search_form, name="search"),
    path('search/result', spoonacular_api_search_view, name="search_result"),
    path('account/dashboard/<int:pk>/set_preferences', set_preferences_form, name="set_dietary_preferences"),
    path('account/dashboard/<int:pk>/view_recipe_recommendations', choose_meals_view, name="view_recipe_recommendations"),
    path('recipe/<int:recipe_id>', view_recipe, name='recipe_view'),
    path('meal/delete/<int:recipe_id>/<int:day>/<int:month>/<int:year>', delete_meal, name='delete_meal'),
    path('blog', blog_post_view, name='blog_post_board'),
    path('blog/add', blog_post_add, name='blog_post_add'),
    path('blog/userPosts/', blog_post_view_user, name='user_posts'),
    path('post/delete/<int:pk>', blog_delete_post, name='delete_post'),
    path('comment/add/<int:pk>', comment_add_view, name="comment_add"),
]
