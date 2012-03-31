from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from item.models import Item
from user_profile.models import UserStatistics

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s agreeing with Review #:%s" % \
            (self.giver.get_full_name(), self.review.id)

class Thank(models.Model):
    giver = models.ForeignKey(User)
    review = models.ForeignKey(Review)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s thanking Review #:%s" \
            (self.giver.get_full_name(), self.review.id)

@receiver(post_save, sender=Review)
def create_review(sender, instance, created, **kwargs):
    if created:
        # Increment the user's review count by one and karma by five
        UserStatistics.objects.filter(pk__exact=instance.user_id).update(
            reviews=F('reviews')+1, karma=F('karma')+5)
        
        # Increment the review's rating by one
        ratings = ['one', 'two', 'three', 'four', 'five']
        field = ratings[instance.rating-1] + '_star'
        setattr(instance.item, field, F(field)+1)
        instance.item.save()

@receiver(post_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
    UserStatistics.objects.filter(pk__exact=instance.user_id).update(
        reviews=F('reviews')-1, karma=F('karma')-5)

    ratings = ['one', 'two', 'three', 'four', 'five']
    field = ratings[instance.rating-1] + '_star'
    setattr(instance.item, field, F(field)-1)
    instance.item.save()
