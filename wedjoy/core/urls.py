from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('signup/',views.userSignupView,name='signup'),
    path('login/',views.userLoginView,name='login'),
    path('logout/',views.custom_logout, name='logout'),
    
    path('userregisteredevents/',views.userregisteredevents, name='userregisteredevents'),
    path('uservolunteering/',views.uservolunteering, name='uservolunteering'),
    path('usercomments/',views.usercomments, name='usercomments'),
    path('usersecurity/',views.usersecurity, name='usersecurity'),
    path('userupdateprofile/',views.userupdateprofile, name='userupdateprofile'),
    
    # -- footer --
    path('contactus/',views.contactus, name='contactus'),
]
