from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class UserLoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
   

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2', )