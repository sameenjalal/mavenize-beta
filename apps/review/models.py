from django.db import models
from django.contrib.auth.models import User
from item.models import Item

class Review(models.Model):
    RATING_CHOICES = [(i,i) for i in range(1,6)] 

    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    text = models.TextField()
    rating = models.SmallIntegerField(choices=RATING_CHOICES)
     
    def __unicode__(self):
        return "%s reviewing Item #%s" % (self.user.get_full_name(),
            self.item.id)

class Agree(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s agreeing with Review #:%s" % \
            (self.giver.get_full_name(), self.review.id)

class Thank(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s thanking Review #:%s" \
            (self.giver.get_full_name(), self.review.id)
