from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Story
from django.contrib import messages
from .forms import StoryForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = StoryForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                story = form.save(commit=False)
                story.user = request.user
                story.save()
                messages.success(request, ("Your Story has been posted!"))
                return redirect('home')
        stories = Story.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"stories": stories, "form": form})
    else:
        stories = Story.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"stories": stories})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profiles_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be logged in to see this page"))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        stories = Story.objects.filter(user_id=pk).order_by("-created_at")

        # POST FORM LOGIC
        if request.method == "POST":
            #GET CURRENT USER ID
            current_user_profile = request.user.profile
            # GET FORM DATA
            action = request.POST['follow']
            # DECIDE TO FOLLOW OR UNFOLLOW
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # SAVE THE PROFILE
            current_user_profile.save()
        return render(request, "profile.html", {"profile": profile, "stories": stories})
    else:
        messages.success(request, ("You must be logged in to see this page"))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been succesfully logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("An error has ocurred. Please try again"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out. We Hope to hear about you again soon!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']
            #LOGIN IN USER AFTER REGISTER
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome now!")
            return redirect('home')
    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_user = Profile.objects.get(user__id=request.user.id)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance= profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Your Profile Has Been Updated")
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form, 'profile_form':profile_form})
    else:
        messages.success(request, "You Must Be Logged In To View This Page")
        return redirect('home')

def story_like(request, pk):
    if request.user.is_authenticated:
        story = get_object_or_404(Story, id=pk)
        if story.likes.filter(id=request.user.id):
            story.likes.remove(request.user)
        else:
            story.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "You Must Be Logged In To View This Page")
        return redirect('home')

def story_show(request, pk):
    story = get_object_or_404(Story, id=pk)
    if story:
        return render(request, "story_show.html", {'story': story})
    else:
        messages.success(request, "That Story Does Not Exist or Has Been Deleted")
        return redirect('home')

def delete_story(request, pk):
    if request.user.is_authenticated:
        story = get_object_or_404(Story, id=pk)
        #CHECK IF THE STORY BELONG TO THIS USER
        if request.user.username == story.user.username:
            story.delete()
            messages.success(request, "Your Story Has Been Deleted")
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, "Please LogIn To Continue")
        return redirect('home')