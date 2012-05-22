from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

import api

@login_required
def find_mavens(request):
    return render_to_response("mavens.html", {},
        RequestContext(request))

@login_required
def mavens(request, page):
    me = request.session['_auth_user_id']
    mavens = api.get_mavens(me)

    return HttpResponse(api.get_user_boxes(me, mavens, page),
        mimetype="application/json")

@login_required
def follow(request, user_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            api.follow(request.session['_auth_user_id'], user_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)
    
    raise Http404

@login_required
def unfollow(request, user_id):
    if request.method == 'DELETE' and request.is_ajax():
        try:
            api.unfollow(request.session['_auth_user_id'], user_id)
            return HttpResponse(status=201)
        except:
            return HttpResponse(status=500)

    raise Http404
    
