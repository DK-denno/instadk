from django.db import models
from django.contrib.auth.models import User
import datetime as dt
# Create your models here.




class Posts(models.Model):
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    postedOn = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user
    class Meta:
        ordering = ['-id']
