from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from users.models import User
from .models import Title
import json


def buy_titles(request):
    """
    POST: a user buys titles by rose or gears
    
    Args:
        request.uid
        request.ttid
    """
    data = json.loads(request.body)
    try:
        user = User.objects.get(id=data['uid'])
        title = Title.objects.get(id=data['ttid'])
    except ObjectDoesNotExist:
        return HttpResponseForbidden("Wrong ID")

    if user.titles_had.filter(id=data['ttid']).exists():
        return HttpResponseForbidden("User already bought this title")

    if title.get_job_display() == 'Taker':
        if user.gear < title.price:
            return HttpResponseForbidden("User's gears not enough")
        user.gear -= title.price
        user.save()
    if title.get_job_display() == 'Rider':
        if user.rose < title.price:
            return HttpResponseForbidden("User's roses not enough") 
        user.rose -= title.price
        user.save()

    user.titles_had.add(title)
    return HttpResponse("Successfully buy new titles")


def equip_title(request):
    """
    POST: a user equip a title

    Args:
        request.uid
        request.ttid
    """
    data = json.loads(request.body)
    try:
        user = User.objects.get(id=data['uid'])
        title = Title.objects.get(id=data['ttid'])
    except ObjectDoesNotExist:
        return HttpResponseForbidden("Wrong ID")
    if user.titles_had.filter(id=title.id).exists():
        user.title_equipped = title
    else:
        return HttpResponseForbidden("User doesn't have such title")
    

def list_titles(request):
    """
    GET: show all titles
    """
    titles = Title.objects.all()
    res = [{
        "ttid" : t.id,
        "name" : t.name,
        "price" : t.price,
        "job" : t.get_job_display()
    } for t in titles]
    return JsonResponse(res, safe=False)


def transfer(request):
    """
    POST: a user transfers roses or gears to another

    Args:
        request.uid
        request.u2id
        request.amount
        request.unit
    """
    data = json.loads(request.body)
    try:
        me = User.objects.get(id=data['uid'])
        him = User.objects.get(id=data['u2id'])
    except ObjectDoesNotExist:
        return HttpResponseForbidden("User not found")

    if data['unit'] == 'rose' and me.rose >= data['amount']:
        me.rose -= data['amount']
        me.save()
        him.rose += data['amount']
        him.save()
        return HttpResponse("Successfully transfered")
    elif data['unit'] == 'gear' and me.gear >= data['amount']:
        me.gear -= data['amount']
        me.save()
        him.gear += data['amount']
        him.save()
        return HttpResponse("Successfully transfered")
    else:
        return HttpResponseForbidden("Failed to transfer")


def rank_taker(request):
    """
    GET: show takers' rank
    """
    rank = User.objects.order_by('-gear')
    res = [{
        'name' : r.name,
        'title' : r.title_equipped.name,
        'gear' : r.gear
    } for r in rank]
    return JsonResponse(res, safe=False)


def rank_rider(request):
    """
    GET: show riders' rank
    """
    rank = User.objects.order_by('-rose')
    res = [{
        'name' : r.name,
        'title' : r.title_equipped.name,
        'rose' : r.gear
    } for r in rank]
    return JsonResponse(res, safe=False)