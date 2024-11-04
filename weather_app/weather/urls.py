from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.getWeather,name='get_weather'),
]