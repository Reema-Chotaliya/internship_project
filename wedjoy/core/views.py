# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib import messages
from .forms import UserSignupForm, UserLoginForm, UserUpdateProfile, UserPasswordChangeForm,  UserPostForm
from django.contrib.auth import update_session_auth_hash, logout
from .models import UserPost

def home(request):
    return render(request, "core/index.html")

def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserSignupForm()
    return render(request, "core/signup.html", {"form": form})

def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                if user.role == "owner":
                    return redirect("localcommunity:business_owner")
                if user.role == "event_organizer":
                    return redirect("localcommunity:eventstudio")
                return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "core/login.html", {"form": form})

def custom_logout(request):
    logout(request)
    return redirect("home")

# ----- user profile -----

@login_required
@role_required(allowed_roles=["user"])
def userupdateprofile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateProfile(request.POST, instance=user)

        if form.is_valid():
            # ✅ directly save profile
            form.save()

            messages.success(request, "Profile updated successfully")
            return redirect("core:userupdateprofile") 

        else:
            print(form.errors)

    else:
        form = UserUpdateProfile(instance=user)

    return render(request, "core/userupdateprofile.html",{"form":form}) 

def userregisteredevents(request):
    # get events registered by current user
    #  registrations model required
    # registrations = EventRegistration.objects.filter(user=request.user)
    
    
    # return render(request, "core/userregisteredevents.html", {
    #     "registrations": registrations
    # })

    return render(request, "core/userregisteredevents.html") 



def uservolunteering(request):
    
    # volunteerings model require
    #  volunteerings = VolunteerRegistration.objects.filter(user=request.user)
    
    #  return render(request, "core/uservolunteering.html", {
    #     "volunteerings": volunteerings
    # })
    
    return render(request, "core/uservolunteering.html")

def usercomments(request):
    
    if request.method == "POST":
        form = UserPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user   # save user
            post.save()
            return redirect('core:usercomments')
    else:
        form = UserPostForm()

    posts = UserPost.objects.all().order_by('-created_at')

    return render(request, "core/usercomments.html", {
        "form": form,
        "posts": posts
    })
 


def usersecurity(request):
    user = request.user

    if request.method == 'POST':
        form = UserPasswordChangeForm(request.POST)

        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect")
                return render(request, "core/usersecurity.html", {"form": form})

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match")
                return render(request, "core/usersecurity.html", {"form": form})

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password updated successfully")
            return redirect("core:usersecurity")   # reload same page

    else:
        form = UserPasswordChangeForm()

    return render(request, "core/usersecurity.html", {"form": form})
    

