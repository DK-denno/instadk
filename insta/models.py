from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField
# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    postedon = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-id']

class Profile(models.Model):
    user = models.OneToOneField(User)
    dp =  models.ImageField(upload_to='images')
    bio = HTMLField(max_length=500)
    posts = models.ForeignKey(Posts, null=True)

    def __str__(self):
        return self.user.username
