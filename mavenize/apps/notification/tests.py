from django.core.cache import get_cache

from user_profile.models import KarmaUser
from item.models import Item
from review.models import Review, Agree, Thank
from bookmark.models import Bookmark
from notification.models import Notification
from social_graph.models import Backward
import nose.tools as nt

class TestNotification(object):
    def setup(self):
        self.writer = KarmaUser.objects.create(username='a')
        self.giver = KarmaUser.objects.create(username='b')
        self.item = Item.objects.create(item_type='pk') # Skip 
        self.review = Review.objects.create(
            user=self.writer, item=self.item, rating=1)

    def test_agree(self):
        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        self.notification = Notification.objects.get(
            sender=self.giver.id)

        # Tests that the recipient is the writer of the review 
        nt.assert_equal(self.notification.recipient_id,
            self.writer.id)
        # Tests that the notice object is the agree
        nt.assert_equal(self.notification.notice_object,
            self.agree)

        self.agree.delete()

        # Tests that the notification has been deleted
        nt.assert_equal(
            list(Notification.objects.filter(
                sender=self.giver.id)),
            [])

    def test_thanks(self):
        self.thanks = Thank.objects.create(
            giver=self.giver, review=self.review)
        self.notification = Notification.objects.get(
            sender=self.giver.id)

        # Tests that the recipient is the writer of the review
        nt.assert_equal(self.notification.recipient_id,
            self.writer.id)
        # Tests that the notice object is the thank
        nt.assert_equal(self.notification.notice_object,
            self.thanks)

        self.thanks.delete()

        # Tests that the notification has been deleted
        nt.assert_equal(
            list(Notification.objects.filter(
                sender=self.giver.id)),
            [])

    def test_following(self):
        self.following = Backward.objects.create(
            destination_id=self.writer.id, source_id=self.giver.id)
        self.notification = Notification.objects.get(
            sender=self.giver.id)

        # Tests that the recipient is the writer of the review
        nt.assert_equal(self.notification.recipient_id,
            self.writer.id)
        # Tests that the notice object is the backward object
        nt.assert_equal(self.notification.notice_object,
            self.following)

        self.following.delete()

        # Tests that the notification object has been deleted
        nt.assert_equal(
            list(Notification.objects.filter(
                sender=self.giver.id)),
            [])

    def test_redis_notification_queue(self):
        cache = get_cache('notifications')
        new_key = "user:" + str(self.writer.id) + ":new"
        recent_key = "user:" + str(self.writer.id) + ":recent"
        cache.delete(new_key)
        cache.delete(recent_key)

        self.agree = Agree.objects.create(
            giver=self.giver, review=self.review)
        
        # Tests that the recent notifications length is one
        nt.assert_equal(cache.get(new_key), 1)
        nt.assert_equal(len(cache.get(recent_key)), 1)

        # Tests the characteristics of the notification
        nt.assert_equal(self.giver.id,
            cache.get(recent_key)[0]['sender_id'])
        nt.assert_equal("agree",
            cache.get(recent_key)[0]['notification_type'])


        self.thanks = Thank.objects.create(
            giver=self.giver, review=self.review)

        # Tests that the recent notifications length is two
        nt.assert_equal(cache.get(new_key), 2)
        nt.assert_equal(len(cache.get(recent_key)), 2)


    def teardown(self):
        self.writer.delete()
        self.giver.delete()
        self.item.delete()
