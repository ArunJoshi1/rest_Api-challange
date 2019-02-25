from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=20,blank=False,)
    body = models.TextField(blank=False)
    image = models.ImageField(blank=True)
    def __str__(self):
        return f'{self.user} post title {self.title}'