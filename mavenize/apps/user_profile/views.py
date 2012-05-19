from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import api

@login_required
def my_profile(request):
    me = request.session['_auth_user_id']
    context = {
        'user': api.get_profile(me)
    }

    return render_to_response("my_profile.html", context,
        RequestContext(request))

@login_required
def profile(request, user_id):
    me = request.session['_auth_user_id'] 
    if int(user_id) == me:
        return redirect('my-profile')

    try:
        context = {
            'user': api.get_profile(user_id),
            'is_following': api.is_following(me, user_id)
        }
    except:
        raise Http404 

    return render_to_response("user_profile.html", context,
        RequestContext(request))

@login_required
def activity(request, user_id, page):
    """
    Returns the list of most recent activities by a user.
    """
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    return HttpResponse(api.get_user_activity(me, [user_id], page),
        mimetype="application/json")

@login_required
def bookmarks(request, user_id, page):
    """
    Returns the list of bookmarks by a user.
    """
    if not request.is_ajax():
        raise Http404

    bookmarked = api.get_bookmarked_items(user_id)
    movies = api.get_movie_thumbnails(
        time_period='month',
        page=page,
        filters={ 'pk__in': bookmarked }
    )
    
    return HttpResponse(movies, mimetype="application/json")

@login_required
def following(request, user_id, page):
    """
    Returns the list of users who the user is following.
    """
    me = request.session['_auth_user_id']
    following = api.get_following(user_id)
    try:
        following.remove(me)
    except:
        pass

    return HttpResponse(api.get_user_boxes(me, following, page),
        mimetype="application/json")

@login_required
def followers(request, user_id, page):
    """
    Returns the list of users who are following the user.
    """
    me = request.session['_auth_user_id']
    followers = api.get_followers(user_id)
    try:
        followers.remove(me)
    except:
        pass

    return HttpResponse(api.get_user_boxes(me, followers, page),
        mimetype="application/json")
