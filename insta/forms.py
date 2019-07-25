from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Posts,Comments,Profile,Likes
from pyuploadcare.dj.forms import ImageField



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', ]

class PostForm(forms.ModelForm):
    image = ImageField()
    class Meta:
        model = Posts
        exclude = ['user','postedon']
        fields = ['caption','image']
       
class Prof(forms.ModelForm):
    dp = ImageField(label='')
    class Meta:
        model=Profile
        exclude=[]
        fields=['dp','bio']


class Comments(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=[]
        fields=['comment']

class Likes(forms.ModelForm):
    class Meta:
        model=Likes
        exclude=[]
        fields=[]
        
