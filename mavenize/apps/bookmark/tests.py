from user_profile.models import KarmaUser
from user_profile.models import UserStatistics
from item.models import Item
from bookmark.models import Bookmark
import nose.tools as nt

class TestBookmark(object):
    def setup(self):
        self.user = KarmaUser.objects.create(username='a')
        self.item = Item.objects.create()

    def test_bookmark(self):
        user_query = UserStatistics.objects.filter(
            pk__exact=self.user.id).values()
        item_query = Item.objects.filter(
            pk__exact=self.item.id).values()
        
        before_create = [dict(user_query[0]), dict(item_query[0])]
        self.bookmark = Bookmark.objects.create(
            user=self.user, item=self.item)
        after_create = [dict(user_query[0]), dict(item_query[0])]

        nt.assert_equal(before_create[0]['bookmarks']+1,
            after_create[0]['bookmarks'])
        nt.assert_equal(before_create[1]['bookmarks']+1,
            after_create[1]['bookmarks'])

        self.bookmark.delete()
        after_delete = [dict(user_query[0]), dict(item_query[0])]

        nt.assert_equal(before_create[0]['bookmarks'],
            after_delete[0]['bookmarks'])
        nt.assert_equal(before_create[1]['bookmarks'],
            after_delete[1]['bookmarks'])

    def teardown(self):
        self.user.delete()
        self.item.delete()

