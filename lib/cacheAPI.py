from django.core.cache import get_cache
from notification.models import Notification

notifications_cache = get_cache('notifications')

"""
GET METHODS
"""

def _get_new_notifications_count(user_id):
    """
    Returns the number of new notifications for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new"
    return notifications_cache.get(new_key)

def _get_notifications(user_id):
    """
    Fetches notifications from the Redis cache.  Returns False
    if there are not enough notifications stored in Redis.
        user_id: primary key of the user (integer)
    """
    recent_key = "user:" + str(user_id) + ":recent"
    raw_notifications = notifications_cache.get(recent_key)
    if not raw_notifications or len(raw_notifications) < 5:
        _cache_notifications_for_user(user_id, 5)
        return notifications_cache.get(recent_key)
    
    return raw_notifications

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
        Notification.objects.select_related('sender') \
                            .prefetch_related('notice_object',
                                'notice_object__review__item') \
                            .filter(recipient=user_id) \
                            .order_by('-created_at')[:num_notifications]
    recent_key = "user:" + str(user_id) + ":recent"
    redis_notifications = [_convert_notification_to_redis_cache(n)
        for n in notifications]
    notifications_cache.set(recent_key, redis_notifications)

def _cache_notification_for_user(notification):
    """
    Caches a single notification for the user.
        notification: Django object (Notification)
    """
    user_id = notification.recipient_id
    recent_key = "user:" + str(user_id) + ":recent"
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
    new_key = "user:" + str(user_id) + ":new"
    notifications_cache.set(new_key, 0)

def _increment_new_notifications_count(user_id):
    """
    Increments the count of new notifications for a user.
        user_id: primary key of the user (integer)
    """
    new_key = "user:" + str(user_id) + ":new"
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
        'notification_type': notification.content_type.__str__(),
        'timestamp': notification.created_at
    }
    if (notification.content_type.__str__() == "thank" or 
            notification.content_type.__str__() == "agree"):
        redis_notification['item_type'] = \
            notification.notice_object.review.item.item_type
        redis_notification['item_name'] = \
            getattr(notification.notice_object.review.item,
                    redis_notification['item_type']).__str__()

    return redis_notification
