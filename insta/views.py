from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts
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
            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})

def profile(request):
    form = PostForm()
    current_user = request.user
    profile = Posts.objects.filter(user=current_user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user=current_user
            post.save()
        return redirect('index')    
    return render(request,'profile/profile.html',{"pics":profile,"form":form})
