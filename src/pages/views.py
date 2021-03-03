from django.http import HttpResponse
from django.shortcuts import render


def homepage_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World. From me Todor</h1>")
