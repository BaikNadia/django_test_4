from django.urls import path
from dogs.apps import DogsConfig
from dogs.views import dogs_list, dogs_detail

app_name = DogsConfig.name

urlpatterns = [
    path('', dogs_list, name='dogs_list'),
    path('dogs/<int:pk>/', dogs_detail, name='dogs_detail')
]
