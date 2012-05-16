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
