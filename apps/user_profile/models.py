from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
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
    user = models.OneToOneField(User, primary_key=True)
    karma = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    bookmarks = models.IntegerField(default=0)
    bookmarks_active = models.IntegerField(default=0)
    agrees_out = models.IntegerField(default=0)
    agrees_in = models.IntegerField(default=0)
    thanks_out = models.IntegerField(default=0)
    thanks_in = models.IntegerField(default=0)

class KarmaUser(User):
    class Meta:
        proxy = True

    def get_statistics(self):
        """
        Returns the UserStatistics model for this user.  Raises
        SiteStatisticsNotAvailable if this site does not allow
        statistics.
        """
        if not hasattr(self, '_statistics_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_STATISTICS_MODULE', False):
                raise SiteStatisticsNotAvailable(
                    'You need to set AUTH_STATISTICS_MODULE in your '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_STATISTICS_MODULE.split('.')
            except ValueError:
                raise SiteStatisticsNotAvailable(
                    'app_label and model_name should be separated by a '
                    'dot in the AUTH_STATISTICS_MODULE setting')
            try:
                model = models.get_model(app_label, models)
                if model is None:
                    raise SiteStatisticsNotAvailable(
                        'Unable to load the statistics model, check '
                        'AUTH_STATISTICS_MODULE in your project settings')
                self._statistics_cache = model._default_manager.using(
                    self._state.db).get(user__id__exact=self.id)
                self._statistics_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteStatisticsNotAvailable
        return self._statistics_cache

