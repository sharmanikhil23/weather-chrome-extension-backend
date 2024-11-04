from django.contrib import admin
from django.urls import path,include
from . import views

import environ

# Initialize the environment variables
env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('',include('geo_location.urls')),
    path('',include('weather.urls'))
]
