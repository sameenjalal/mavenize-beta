from django.core.cache import get_cache

from notification.models import Notification
from user_profile.models import KarmaUser
from social_graph.models import Backward
import nose.tools as nt

class TestSocialGraph(object):
    def setup(self):
        self.follower = KarmaUser.objects.create(username='a')
        self.following = KarmaUser.objects.create(username='b')

    def test_notification(self):
        """
        Tests to see if a notification was created and deleted after
        a following relationship is created and deleted.
        """
        cache = get_cache('notifications')
        before_follow = cache.get('user:'+str(self.following.id)+':new') or 0

        self.follow = Backward.objects.create(
            destination_id=self.following.id,
            source_id=self.follower.id
        )
        self.notification = Notification.objects.get(
            sender=self.follower,
            recipient=self.following
        )

        # Tests that a notification was created
        nt.assert_true(self.notification)
        nt.assert_equal(self.follow.pk,
                        self.notification.object_id)
        # Tests that the new notification count increased
        nt.assert_equal(before_follow+1,
            cache.get('user:'+str(self.following.id)+':new'))

        self.follow.delete()
        self.notification = Notification.objects.filter(
            sender=self.follower,
            recipient=self.following
        )

        # Tests that the notification was deleted.
        nt.assert_false(self.notification)

    def teardown(self):
        self.follower.delete()
        self.following.delete()
