from django.db import models
from django.contrib.auth.models import User

class Gender(models.Model):
    gender = models.IntegerField()
    text = models.CharField(max_length=6)

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    avator = models.FileField(null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)

    nickname = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


