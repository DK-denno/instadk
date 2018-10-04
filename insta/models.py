from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Posts(models.Model):
    user = models.ForeignKey(User)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.user
    class Meta:
        ordering = ['-id']
