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
from django.urls import path
from pages.views import homepage_view, bmi_calculator_view, contact_view
from account.views import registration_view, logout_view, login_view, dashboard_view
from progress.views import progress_form_view, UpdateProgressView
from recipes.views import spoonacular_api_search_view, spoonacular_api_search_form
from diets.views import set_preferences_form, view_recipe_preferences_view


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
    path('account/dashboard/<int:pk>', dashboard_view, name='user_dashboard'),
    path('search/', spoonacular_api_search_form, name="search"),
    path('search/result', spoonacular_api_search_view, name="search_result"),
    path('account/dashboard/<int:pk>/set_preferences', set_preferences_form, name="set_dietary_preferences"),
    path('account/dashboard/<int:pk>/view_recipe_preferences', view_recipe_preferences_view, name="view_recipe_preferences")
]
