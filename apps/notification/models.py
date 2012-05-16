from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from item.models import Item

class Notification(models.Model):
    sender = models.ForeignKey(User,
        related_name="notifications_sent")
    recipient = models.ForeignKey(User,
        related_name="notifications_received")
    notification_type = models.CharField(max_length=10)
    item = models.ForeignKey(Item, null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __unicode__(self):
        return "User %s sending notifcation to User %s" % \
            (self.sender_id, self.recipient_id)
