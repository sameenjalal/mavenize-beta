from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from social_auth.models import UserSocialAuth

import facebook

"""
Models
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ImageField(
        upload_to='img/users/avatars',
        default='img/users/avatars/default.jpg',
    )
    thumbnail = models.ImageField(
        upload_to='img/users/thumbnails',
        default='img/users/thumbnails/default.jpg',
    )
    gender = models.CharField(max_length=1)
    about_me = models.CharField(max_length=80, default='')

    class Meta:
        verbose_name_plural = "User Profiles"

    def __unicode__(self):
        return self.user.get_full_name()

class UserStatistics(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    karma = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    agrees_out = models.IntegerField(default=0)
    agrees_in = models.IntegerField(default=0)
    thanks_out = models.IntegerField(default=0)
    thanks_in = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "User Statistics"

    def __unicode__(self):
        return "%s: %s" % (self.user.get_full_name(), self.karma)

class KarmaUser(User):
    class Meta:
        proxy = True

    def get_statistics(self):
        """
        Returns the UserStatistics model for this user.
        """
        if not hasattr(self, '_statistics_cache'):
            try:
                self._statistics_cache = UserStatistics.objects.get( 
                    user__id__exact=self.id)
                self._statistics_cache.user = self
            except:
                raise ObjectDoesNotExist 
        return self._statistics_cache

"""
Signals
"""
@receiver(pre_update, sender=FacebookBackend)
def update_user_profile(sender, user, response, details, **kwargs):
    from signalAPI import create_user_profile
    create_user_profile(user.id, response.get('id'))
  
@receiver(post_save, sender=KarmaUser)
def create_karma_user(sender, instance, created, **kwargs):
    """
    Create a user profile and user statistics for this user.
    """
    if created:
        UserProfile.objects.create(user=instance)
        UserStatistics.objects.create(user=instance)
