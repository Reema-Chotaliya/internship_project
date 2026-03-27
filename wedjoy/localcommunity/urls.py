# localcommunity/urls.py
from django.urls import path
from . import views

app_name = "localcommunity"

urlpatterns = [
    path("businessowner/", views.business_owner_dashboard, name="business_owner"),
    path("user/", views.user_dashboard, name="user_dashboard"),
    path("eventstudio/", views.eventstudio, name="eventstudio"),
    
    path('addbusiness/', views.addbusiness, name='addbusiness'),
    path('analyticsbusiness/', views.analyticsbusiness, name='analyticsbusiness'),
    path("businessownerdashboard/", views.businessownerdashboard, name="businessownerdashboard"),
    path('mybusinesses/', views.mybusinesses, name='mybusinesses'),
    path('reviews/', views.reviews, name='reviews'),
    path('settingsbusiness/', views.settingsbusiness, name='settingsbusiness'),
    path('logoutbusiness/', views.logoutbusiness, name='logoutbusiness'),
    
    path("eventstudiodashboard/", views.eventstudiodashboard, name="eventstudiodashboard"),
    path('myevents/', views.myevents, name='myevents'), 
    path('createevent/', views.createevent, name='createevent'),
    path('attendeesevent/', views.attendeesevent, name='attendeesevent'),
    # path('analyticsevent/', views.analyticsevent, name='analyticsevent'),
    path('settingsevent/', views.settingsevent, name='settingsevent'),
    path('logoutevent/', views.logoutevent, name='logoutevent'),
    
]