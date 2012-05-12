from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from social_auth.signals import socialauth_registered 
from social_auth.backends.facebook import FacebookBackend
from social_auth.models import UserSocialAuth

from notification.models import Notification

import signalAPI

class Forward(models.Model):
    source_id = models.BigIntegerField(db_index=True)
    destination_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)

class Backward(models.Model):
    destination_id = models.BigIntegerField(db_index=True)
    source_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)

@receiver(socialauth_registered, sender=None)
def new_user(sender, user, response, details, **kwargs):
    """
    Update user social graph using Facebook friends.
    """
    user.is_new = True
    signalAPI.build_social_graph(user.id)
    return False

@receiver(post_save, sender=Backward)
def follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender_id=instance.source_id,
            recipient_id=instance.destination_id,
            notice_object=instance
        )

@receiver(post_delete, sender=Backward)
def unfollow_notification(sender, instance, **kwargs):
    """
    Delete the notification that was already created.
    """
    Notification.objects.get(
        sender_id=instance.source_id,
        recipient_id=instance.destination_id,
        object_id=instance.id
    ).delete()
