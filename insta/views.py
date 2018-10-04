from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts
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
    current_user = request.user
    profile = Posts.objects.filter(user=current_user)
    return render(request,'profile.html',{"pics":profile})