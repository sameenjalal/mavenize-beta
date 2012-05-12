from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import get_model

from review.models import Review
import api

@login_required
def review(request, title, app, model):
    if request.method == 'POST':
        model_object = get_model(app, model)
        review_item = get_object_or_404(model_object, url=title)
        api.review(
            user_id=request.session['_auth_user_id'],
            item_id=review_item.pk,
            text=request.POST['text'],
            rating=int(request.POST['rating'])
        )
    
    return redirect(request.META.get('HTTP_REFERER', None))


@login_required
def agree(request, review_id):
    if request.method == 'POST' and request.is_ajax():
        error = api.agree(
            user_id=request.session['_auth_user_id'],
            review_id=review_id
        )
        
        if not error:
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=500)
    return HttpResponse(status=403)


@login_required
def disagree(request, review_id):
    if request.method == 'POST' and request.is_ajax():
        error = api.review(
            user_id=request.session['_auth_user_id'],
            item_id=get_object_or_404(Review, pk=review_id).item_id,
            text=request.POST['text'],
            rating=int(request.POST['rating'])
        )

        if not error:
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=500)
    return HttpResponse(status=403)


@login_required
def thank(request, review_id):
    if request.method == 'POST' and request.is_ajax():
        error = api.thank(
            user_id=request.session['_auth_user_id'],
            review_id=review_id,
            note=request.POST['text']
        )

        if not error:
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=500)
    return HttpResponse(status=403)

