from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from haystack.forms import SearchForm
from haystack.views import SearchView

import nexus

admin.autodiscover()
nexus.autodiscover()

urlpatterns = patterns('activity_feed.views',
    url(r'^$', 'index', name='index'),

    url(r'^feed/(?P<page>\d+)/$', 'activity'),
)

urlpatterns += patterns('haystack.views',
    url(r'^movies/search/$', SearchView(template='movie_search.html',
        form_class=SearchForm), name='movie-search')
)

urlpatterns += patterns('user_profile.views',
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^signup/complete$', 'complete_signup'),
    url(r'^me/$', 'my_profile', name='my-profile'),
    url(r'^users/(?P<user_id>\d+)/$', 'profile', name='user-profile'),

    url(r'^users/(?P<user_id>\d+)/raves/(?P<page>\d+)/$', 'activity'),
    url(r'^users/(?P<user_id>\d+)/marks/(?P<page>\d+)/$', 'bookmarks'),
    url(r'^users/(?P<user_id>\d+)/following/(?P<page>\d+)/$', 'following'),
    url(r'^users/(?P<user_id>\d+)/followers/(?P<page>\d+)/$', 'followers'),
)

urlpatterns += patterns('movie.views',
    url(r'^movies/$', 'explore', name='movie-explore'),
    url(r'^movies/(?P<title>[-\w]+)/$', 'profile', name="movie-profile"),

    url(r'^movies/(?P<title>[-\w]+)/synopsis$', 'synopsis'),
    url(r'^movies/genres/all$', 'genres'),
    url(r'^movies/cast/all$', 'cast'),
    url(r'^movies/(?P<time_period>\w+)/(?P<page>\d+)/$', 'explore'),
)

urlpatterns += patterns('review.views',
    url(r'^movies/(?P<title>[-\w]+)/review/$', 'review',
        {'app': 'movie', 'model': 'movie'}),
    
    url(r'^rerave/(?P<review_id>\d+)/$', 'agree'),
    url(r'^disagree/(?P<review_id>\d+)/$', 'disagree'),
    url(r'^thank/(?P<review_id>\d+)/$', 'thank'),
)

urlpatterns += patterns('social_graph.views',
    url(r'^mavens/$', 'find_mavens'),
    url(r'^mavens/(?P<page>\d+)/$', 'mavens'),

    url(r'^follow/(?P<user_id>\d+)/$', 'follow'),
    url(r'^unfollow/(?P<user_id>\d+)/$', 'unfollow'),
)

urlpatterns += patterns('bookmark.views',
    url(r'^bookmark/(?P<item_id>\d+)/$', 'bookmark'),
    url(r'^unbookmark/(?P<item_id>\d+)/$', 'unbookmark'),

    url(r'^bookmarks/count/$', 'new_bookmarks'),
    url(r'^bookmarks/(?P<page>\d+)/$', 'bookmarks'),
    url(r'^bookmarks/item/(?P<item_id>\d+)/$', 'friend_bookmarks'),
)

urlpatterns += patterns('notification.views',
    url(r'^notifications/count/$', 'new_notifications'),
    url(r'^notifications/recent/$', 'recent_notifications'),
    url(r'^notifications/(?P<page>\d+)/$', 'notifications'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^nexus/', include(nexus.site.urls)),
    url(r'', include('social_auth.urls')),
)

if settings.STATIC_MEDIA_SERVER:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': 'mavenize/media'}),
)
