from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Posts,Comments,Profile



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['user','postedon']
        fields = ['caption','image']
       
class Prof(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=[]
        fields=['dp','bio']


class Comments(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=[]
        fields=['comment']