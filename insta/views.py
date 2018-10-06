from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts,Profile,Follow
from .forms import PostForm,Prof
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse


# Create your views here.

def index(request):
    post = Posts.objects.all()
    follow = Follow.objects.filter(current_user=request.user)
    if follow:
        follow=Follow.objects.get(current_user=request.user)
        followers=follow.users.all()
        return render(request,'index.html', {"followers":followers,"post":post})
    return render(request,'index.html', {"post":post})




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
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'reg.html', {'form': form})

def profile(request):
    form = PostForm()
    prof_form=Prof()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    posts = Posts.objects.filter(user=current_user)
    follow = Follow.objects.filter(current_user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        prof_form=Prof(request.POST,request.FILES,instance=current_user.profile)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user
            post.profile=profile
            post.save()
            return redirect('index') 
        if prof_form.is_valid():
            prof_form.save()
            return redirect('profile')  
    if follow:
        follow=Follow.objects.get(current_user=request.user)
        followers=follow.users.all()      
        return render(request,'profile/profile.html',{"pics":posts,"profile":profile,"prof":prof_form,"followers":followers,"form":form})
        


def profiles(request,id):
    profile = Profile.objects.filter(user_id=id)
    posts=Posts.objects.filter(user_id=request.user.id)
    if follow:
        follow=Follow.objects.get(current_user=request.user)
        followers=follow.users.all()
    
    return render(request,'profile/profiles.html',{"profile":profile,"pics":posts})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def follow(request,operation,id):
    user=User.objects.get(id=id)   
    if operation=='follow':
        Follow.follow(request.user,user)
        return redirect('index')
    elif operation=='unfollow':
        Follow.unfollow(request.user,user)
        return redirect('index')


