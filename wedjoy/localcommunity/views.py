# localcommunity/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required

@login_required
@role_required(allowed_roles=["owner"])
def business_owner_dashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")

@login_required
@role_required(allowed_roles=["user"])
def user_dashboard(request):
    return render(request, "core/index.html")

def eventstudio(request):
    return render(request, "localcommunity/eventstudio/eventstudio.html")

def businessownerdashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")
def mybusinesses(request):
    return render(request, "localcommunity/businessowner/mybusinesses.html")
def addbusiness(request):
    return render(request, "localcommunity/businessowner/addbusiness.html")
def reviews(request):
    return render(request, "localcommunity/businessowner/reviews.html") 
def analyticsbusiness(request):
    return render(request, "localcommunity/businessowner/analytics.html")
def settingsbusiness(request):
    return render(request, "localcommunity/businessowner/settings.html")
def logoutbusiness(request):
    return render(request, "core/index.html")

def eventstudiodashboard(request):
    return render(request, "localcommunity/eventstudio/eventstudio.html")
def myevents(request):
    return render(request, "localcommunity/eventstudio/myevents.html")
def createevent(request):
    return render(request, "localcommunity/eventstudio/createevent.html") 
def attendeesevent(request):
    return render(request, "localcommunity/eventstudio/attendeesevent.html")
def analyticsevent(request):
    return render(request, "localcommunity/eventstudio/analyticsbusiness.html")
def settingsevent(request):
    return render(request, "localcommunity/eventstudio/settingsevent.html")
def logoutevent(request):
    return render(request, "core/index.html")