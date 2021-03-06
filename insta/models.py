from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from pyuploadcare.dj.models import ImageField
from tinymce.models import HTMLField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    dp = ImageField(blank=True, manual_crop="")
    bio = HTMLField(max_length=500)
    email_confirmed = models.BooleanField(default=False)

    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
    
    def __str__(self):
        return self.user.username

class Posts(models.Model):
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=250)
    image = ImageField(blank=True, manual_crop="")
    postedon = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile,null=True)
    
    
    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-id']
    
    @classmethod
    def save_post(self):
        self.save()
    @classmethod
    def get_posts(cls):
         posts = cls.objects.all()
         return posts
    @classmethod
    def delete_post(self):
        self.delete()
    
    def save_image(self):
        self.save()

    @classmethod
    def delete_image_by_id(cls, id):
        pictures = cls.objects.filter(pk=id)
        pictures.delete()

    @classmethod
    def get_image_by_id(cls, id):
        pictures = cls.objects.get(pk=id)
        return pictures


    
    

class Comments(models.Model):
    user = models.ForeignKey(User)
    post=models.ForeignKey(Posts,related_name='comments')
    comment=models.CharField(max_length=200)

class Likes(models.Model):
    user = models.OneToOneField(User,related_name='l_user')
    post=models.ForeignKey(Posts,related_name='likes')
    like=models.CharField(max_length=3,default='1')
     


class Follow(models.Model):
    users=models.ManyToManyField(User,related_name='follow')
    current_user=models.ForeignKey(User,related_name='c_user',null=True)

    @classmethod
    def follow(cls,current_user,new):
        friends,created=cls.objects.get_or_create(current_user=current_user)
        friends.users.add(new)
    
    @classmethod
    def unfollow(cls,current_user,new):
        friends,created=cls.objects.get_or_create(current_user=current_user)
        friends.users.remove(new)

