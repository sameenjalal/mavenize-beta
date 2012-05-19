from django.core.cache import get_cache
from notification.models import Notification

import datetime as dt

notifications_cache = get_cache('notifications')

"""
GET METHODS
"""

def _get_new_notifications_count(user_id):
    """
    Returns the number of new notifications for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new.notifications"
    return notifications_cache.get(new_key)


def _get_notifications(user_id):
    """
    Fetches notifications from the Redis cache.  Returns False
    if there are not enough notifications stored in Redis.
        user_id: primary key of the user (integer)
    """
    recent_key = "user:" + str(user_id) + ":recent.notifications"
    raw_notifications = notifications_cache.get(recent_key)
    if not raw_notifications or len(raw_notifications) < 5:
        _cache_notifications_for_user(user_id, 5)
        return notifications_cache.get(recent_key)
    
    return raw_notifications


def _get_new_bookmarks_count(user_id):
    """
    Returns the number of new relevant bookmarks for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new.bookmarks"
    return notifications_cache.get(new_key)

def _get_bookmarks_last_checked(user_id):
    """
    Returns the datetime of the last time the user checked their
    bookmarks.
        user_id: primary key of the user (integer)
    """
    time_key = "user:" + str(user_id) + ":last.checked.bookmarks"
    return notifications_cache.get(time_key)


"""
CREATE METHODS
"""
def _cache_notifications_for_user(user_id, num_notifications):
    """
    Fetches a specified number of notifications from the postgres
    database and stores them in the Redis cache.
        user_id: primary key of the user (integer)
        num_notifications: number of notifications to retrieve
            (integer)
    """
    notifications = \
        Notification.objects.select_related('sender',
                                            'item',
                                            'item__movie') \
                            .filter(recipient=user_id) \
                            .order_by('-created_at')[:num_notifications]
    recent_key = "user:" + str(user_id) + ":recent.notifications"
    redis_notifications = [_convert_notification_to_redis_cache(n)
        for n in notifications]
    notifications_cache.set(recent_key, redis_notifications)

def _cache_notification_for_user(notification):
    """
    Caches a single notification for the user.
        notification: Django object (Notification)
    """
    user_id = notification.recipient_id
    recent_key = "user:" + str(user_id) + ":recent.notifications"
    recent_notifications = notifications_cache.get(recent_key)
    if not recent_notifications or len(recent_notifications) < 5:
        _cache_notifications_for_user(user_id, 5)
    else:
        to_insert = _convert_notification_to_redis_cache(
            notification)
        recent_notifications.pop()
        recent_notifications.insert(0, to_insert)
        notifications_cache.set(recent_key,
                                recent_notifications)


"""
UPDATE METHODS
"""
def _reset_new_notifications_count(user_id):
    """
    Resets the number of new notifications for a user to zero.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new.notifications"
    notifications_cache.set(new_key, 0)

def _increment_new_notifications_count(user_id):
    """
    Increments the count of new notifications for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new.notifications"
    notifications_cache.incr(new_key)

def _reset_new_bookmarks_count(user_id):
    """
    Resets the number of new bookmarks for a user to zero.
        user_id: primary key of the user (integer)
    """
    data = {
        "user:" + str(user_id) + ":new.bookmarks": 0,
        "user:" + str(user_id) + ":last.checked.bookmarks": \
            dt.datetime.now()
    }
    notifications_cache.set_many(data, 0)

def _increment_new_bookmarks_count(user_id):
    """
    Increments the count of new bookmarks for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new.bookmarks"
    notifications_cache.incr(new_key)


"""
HELPER METHODS
"""
def _convert_notification_to_redis_cache(notification):
    """
    Converts a notification into a Python dictionary
    that will be stored in the Redis cache.
        notification: Notification object 
    """
    redis_notification = {
        'sender_id': notification.sender_id,
        'sender_name': notification.sender.get_full_name(),
        'notification_type': notification.notification_type,
        'timestamp': notification.created_at
    }
    if (notification.notification_type == "thank" or 
            notification.notification_type == "agree"):
        redis_notification['item_type'] = notification.item.item_type
        redis_notification['item_name'] = \
            getattr(notification.item,
                    redis_notification['item_type']).__str__()

    return redis_notification
