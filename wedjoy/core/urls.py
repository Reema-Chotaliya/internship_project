from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('signup/',views.userSignupView,name='signup'),
    path('login/',views.userLoginView,name='login'),
    path('logout/',views.custom_logout, name='logout'),
]
