from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from item.models import Item

import api


class Bookmark(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s bookmarking Item #%s" % (self.user.get_full_name(),
            self.item.id)


class BookmarkGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    bookmarks = models.ManyToManyField(Bookmark)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "'%s' owned by: %s" % (self.name,
            self.user.get_full_name())


@receiver(post_save, sender=Bookmark)
def create_bookmark(sender, instance, created, **kwargs):
    """
    Increment the user and item's bookmarks by one.
    """
    if created:
        api.update_statistics(
            model_name="userstatistics",
            obj_id=instance.user_id,
            bookmarks=1
        )
        api.update_statistics(
            model_name="item",
            obj_id=instance.item_id,
            bookmarks=1
        )


@receiver(post_delete, sender=Bookmark)
def delete_bookmark(sender, instance, **kwargs):
    """
    Undo the updates of the bookmark.
    """
    api.update_statistics(
        model_name="userstatistics",
        obj_id=instance.user_id,
        bookmarks=-1
    )
    api.update_statistics(
        model_name="item",
        obj_id=instance.item_id,
        bookmarks=-1
    )
