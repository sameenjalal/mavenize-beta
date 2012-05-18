from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import api

@login_required
def bookmark(request, item_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            api.bookmark(request.session['_auth_user_id'], item_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)

    raise Http404

@login_required
def unbookmark(request, item_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            api.unbookmark(request.session['_auth_user_id'], item_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)

    raise Http404

@login_required
def new_bookmarks(request):
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    return HttpResponse(api.get_new_bookmarks_count(me),
        mimetype="application/json")

@login_required
def bookmarks(request, page):
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    response = api.get_bookmarked_movies(me, page)
    if int(page) == 1:
        api.reset_new_bookmarks_count(me)
    return HttpResponse(response, mimetype="application/json")

@login_required
def friend_bookmarks(request, item_id):
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    return HttpResponse(api.get_friend_bookmarks(me, item_id),
        mimetype="application/json")
