from django.urls import path
from .views import *
from django.urls import path

app_name = 'anagram'

urlpatterns = [
    path('', SearchFormView.as_view(), name='search'),
    ]
