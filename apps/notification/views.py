from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import api

@login_required
def new_notifications(request):
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    return HttpResponse(api.get_new_notifications_count(me),
        mimetype="application/json")

@login_required
def recent_notifications(request):
    me = request.session['_auth_user_id']
    api.reset_new_notifications_count(me)
    return HttpResponse(api.get_recent_notifications(me),
        mimetype="application/json")

@login_required
def notifications(request, page):
    """
    Returns the list of notifications for the logged in user.
    """
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    return HttpResponse(api.get_notifications(me, page),
        mimetype="application/json")
