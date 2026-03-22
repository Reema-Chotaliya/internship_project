from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib import messages

from .decorators import role_required
from .forms import OwnerProfileUpdateForm , EventProfileUpdateForm


# ================= DASHBOARDS =================

@login_required
@role_required(allowed_roles=["owner"])
def business_owner_dashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")


@login_required
@role_required(allowed_roles=["user"])
def user_dashboard(request):
    return render(request, "core/index.html")


# ================= BUSINESS OWNER PAGES =================

def businessownerdashboard(request):
    return render(request, "localcommunity/businessowner/businessowner.html")


def mybusinesses(request):
    return render(request, "localcommunity/businessowner/mybusinesses.html")


def addbusiness(request):
    return render(request, "localcommunity/businessowner/addbusiness.html")


def reviews(request):
    return render(request, "localcommunity/businessowner/reviews.html")


def analyticsbusiness(request):
    return render(request, "localcommunity/businessowner/analyticsbusiness.html")


# ================= SETTINGS (FIXED) =================

@login_required
@role_required(allowed_roles=["owner"])
def settingsbusiness(request):

    user = request.user

    if request.method == 'POST':
        form = OwnerProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():

            # ✅ DON'T SAVE YET
            user_obj = form.save(commit=False)

            # password fields
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            # 👉 if user trying to change password
            if current_password or new_password or confirm_password:

                if not user.check_password(current_password):
                    messages.error(request, "Current password is incorrect")
                    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match")
                    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})

                # ✅ set new password
                user_obj.set_password(new_password)

                # save BEFORE updating session
                user_obj.save()

                # keep user logged in
                update_session_auth_hash(request, user_obj)

                messages.success(request, "Password updated successfully")

            else:
                # ✅ save normal profile updates
                user_obj.save() 
                messages.success(request, "Profile updated successfully")

            return redirect('localcommunity:businessownerdashboard')

        else:
            print(form.errors)

    else:
        form = OwnerProfileUpdateForm(instance=user)

    return render(request, 'localcommunity/businessowner/settingsbusiness.html', {"form": form})


# ================= LOGOUT =================

def logoutbusiness(request):
    logout(request)
    return redirect('login')  # change to your login URL name


# ================= EVENT STUDIO =================

def eventstudio(request):
    return render(request, "localcommunity/eventstudio/eventstudio.html")


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

@login_required
@role_required(allowed_roles=["event_organizer"])
def settingsevent(request):
    
    user = request.user

    if request.method == 'POST':
        form = EventProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():

            user_obj = form.save(commit=False)

            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if current_password or new_password or confirm_password:

                if not user.check_password(current_password):
                    messages.error(request, "Current password is incorrect")
                    return render(request, 'localcommunity/eventstudio/settingsevent.html', {"form": form})

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match")
                    return render(request, 'localcommunity/eventstudio/settingsevent.html', {"form": form})

                user_obj.set_password(new_password)
                user_obj.save()
                update_session_auth_hash(request, user_obj)

                messages.success(request, "Password updated successfully")

            else:
                user_obj.save()
                messages.success(request, "Profile updated successfully")

            return redirect('localcommunity:eventstudiodashboard')

        else:
            print(form.errors)

    else:
        form = EventProfileUpdateForm(instance=user)
    
    # ✅ FIX IS HERE
    return render(request, "localcommunity/eventstudio/settingsevent.html", {"form": form})


def logoutevent(request):
    logout(request)
    return redirect('login')  # change if needed