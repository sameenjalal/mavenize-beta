from django.http import HttpResponse
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
    if not request.is_ajax():
        raise Http404

    me = request.session['_auth_user_id']
    api.reset_new_notifications_count(me)
    return HttpResponse(api.get_recent_notifications(me),
        mimetype="application/json")
