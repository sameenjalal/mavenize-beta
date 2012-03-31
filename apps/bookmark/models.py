from django.db import models
from django.contrib.auth.models import User

from item.models import Item

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    is_public = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s bookmarking Item #%s" % (self.user.get_full_name(),
            self.item.id)
