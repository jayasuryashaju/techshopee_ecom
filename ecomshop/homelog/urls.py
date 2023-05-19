
from django.urls import path
from . import views

app_name = 'homelog'

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),

]