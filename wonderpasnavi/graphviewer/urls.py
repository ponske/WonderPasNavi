from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list')
]
