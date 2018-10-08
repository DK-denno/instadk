from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts,Profile,Follow
from .forms import PostForm,Prof,Comments,Likes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    post = Posts.objects.all()
    comm = Comments()
    like = Likes()
    return render(request,'index.html', {"post":post,"like":like,"comm":comm})




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
@login_required(login_url='/auth/login')
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
    return render(request,'profile/profile.html',{"pics":posts,"profile":profile,"prof":prof_form,"form":form})
        

@login_required(login_url='/auth/login')
def profiles(request,id):
    profile = Profile.objects.get(user_id=id)
    print(profile.user)
    posts=Posts.objects.filter(user_id=request.user.id)
    follow=Follow.objects.filter(current_user=request.user)
    if follow:
        follow=Follow.objects.get(current_user=request.user)
        followers=follow.users.all()
        for c_user in followers:
            if c_user.id == request.user.id:
                unfollow='unfollow'
                return render(request,'profile/profiles.html',{"profile":profile,"pics":posts,"unfollow":unfollow})
            else:
                follow='follow'    
                return render(request,'profile/profiles.html',{"profile":profile,"pics":posts,"follow":follow})
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

@login_required(login_url='/auth/login')
def comment(request,id):
    post = Posts.objects.get(id=id)
    if request.method == 'POST':
        comm=Comments(request.POST)
        if comm.is_valid():
            comment=comm.save(commit=False)
            comment.user = request.user
            comment.post=post
            comment.save()
            return redirect('index')
    return redirect('index')

@login_required(login_url='/auth/login')
def likes(request,id):
    likes=Posts.objects.get(id=id)
    if request.method == 'POST':

        like = Likes(request.POST)
        if like.is_valid():
            liked=like.save(commit=False)
            # already_liked = Likes.objects.all()
            # for user in already_liked.user:
            #     if user==request.user:
            #        user.delete()
            #     else:
                    
            liked.user = request.user
            liked.post = likes
            liked.save()
            return redirect('index')   
    return redirect('index')


