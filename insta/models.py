from django.db import models
from django.contrib.auth.models import User
import datetime as dt
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User)
    dp = models.ImageField(upload_to='images')
    bio = models.CharField(max_length=500)



class Posts(models.Model):
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    postedOn = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user.username
    class Meta:
        ordering = ['-id']
