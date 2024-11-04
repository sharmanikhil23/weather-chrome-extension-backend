from django.urls import path
from . import views

urlpatterns = [
    path('geolocation/', views.getGeolocation,name='get_geolocation'),
]