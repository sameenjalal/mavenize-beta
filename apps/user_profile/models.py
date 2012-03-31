from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ImageField(
        upload_to='img/users/avatars',
        default='img/users/avatars/default.jpg',
    )
    thumbnail = models.ImageField(
        upload_to='img/users',
        default='img/users/thumbnails/default.jpg',
    )
    gender = models.CharField(max_length=1)

    def __unicode__(self):
        return self.user.get_full_name()

class UserStatistics(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    karma = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    bookmarks_active = models.IntegerField(default=0)
    agrees_out = models.IntegerField(default=0)
    agrees_in = models.IntegerField(default=0)
    thanks_out = models.IntegerField(default=0)
    thanks_in = models.IntegerField(default=0)

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

