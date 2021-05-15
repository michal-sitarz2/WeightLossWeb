from django.urls import path

from .views import articles_view

urlpatterns = [
    path('articles', articles_view)
]
