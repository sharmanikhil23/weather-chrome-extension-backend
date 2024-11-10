from django.contrib import admin
from django.urls import path,include
from . import views

import environ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main),
    path('getweather/',views.home),   
]
