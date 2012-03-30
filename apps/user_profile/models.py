from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(
        upload_to='img/users/avatars',
        default='img/users/avatars/default.jpg'
    )
    thumbnail = models.ImageField(
        upload_to='img/users',
        default='img/users/thumbnails/default.jpg'
    )
    gender = models.CharField(max_length=1)

class UserStatistics(models.Model):
    user = models.OneToOneField(User)
    karma = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    bookmarks_active = models.IntegerField(default=0)
    agrees_out = models.IntegerField(default=0)
    agrees_in = models.IntegerField(default=0)
    thanks_out = models.IntegerField(default=0)
    thanks_in = models.IntegerField(default=0)
