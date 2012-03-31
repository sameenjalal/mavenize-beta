from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    five_star = models.IntegerField(default=0)
    four_star = models.IntegerField(default=0)
    three_star = models.IntegerField(default=0)
    two_star = models.IntegerField(default=0)
    one_star = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id)

class Link(models.Model):
    item = models.ForeignKey(Item)
    partner = models.CharField(max_length=20)
    url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.url
