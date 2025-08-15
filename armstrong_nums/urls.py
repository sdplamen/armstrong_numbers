from django.urls import path
from armstrong_nums import views

urlpatterns = [
    path('', views.armstrong_numbers_view, name='index'),
]