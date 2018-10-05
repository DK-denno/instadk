from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts,Profile
from .forms import PostForm

# Create your views here.

def index(request):
    post = Posts.objects.all()
    return render(request,'index.html',{"post":post})



def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,email=email, password=raw_password)
            profile = Profile(user=user)
            profile.save()
            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})

def profile(request):
    form = PostForm()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    posts = Posts.objects.filter(user=current_user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user
            post.profile=profile
            post.save()
            return redirect('index')   
        
    return render(request,'profile/profile.html',{"pics":posts,"profile":profile,"form":form})


def profiles(request,id):
    profile = Profile.objects.filter(user_id=id)
    return render(request,'profile/profiles.html',{"profile":profile})
