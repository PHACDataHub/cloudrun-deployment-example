from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('hello_city/<str:city_name>/', views.hello_city, name='hello_city'),
    path("add_city", views.add_city, name='add_city'),
    path('delete_city', views.delete_city, name='delete_city'),
    path('hello', views.hello, name="hello_world")
]