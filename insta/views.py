from django.shortcuts import render
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts
# Create your views here.

def index(request):
    return render(request,'index.html')



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
            login(user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})

def home(request):
    post = Posts.Objects.all()