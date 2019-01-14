from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.conf import settings
from django.utils import timezone
from users.models import User
from .models import Title
import json
import os
from datetime import datetime



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
        print("Wrong ID")
        return HttpResponseForbidden()

    if user.titles_had.filter(id=data['ttid']).exists():
        print("User already bought this title")
        return HttpResponseForbidden()

    if title.get_job_display() == 'Taker':
        if user.gear < title.price:
            print("User's gears not enough")
            return HttpResponseForbidden()
        user.gear -= title.price
        user.save()
    if title.get_job_display() == 'Rider':
        if user.rose < title.price:
            print("User's roses not enough")
            return HttpResponseForbidden() 
        user.rose -= title.price
        user.save()

    user.titles_had.add(title)
    print("Successfully buy new titles")
    return HttpResponse()


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
        print("Wrong ID")
        return HttpResponseForbidden()
    if user.titles_had.filter(id=title.id).exists():
        user.title_equipped = title
        user.image = request.build_absolute_uri(title.image.url)
       
        user.save()
        print("Successfully equipped")
        return HttpResponse()
    else:
        print("User doesn't have such title")
        return HttpResponseForbidden()
    

def list_titles(request):
    """
    GET: show all titles
    """
    titles = Title.objects.all()
    res = [{
        "ttid" : t.id,
        "name" : t.name,
        "price" : t.price,
        "job" : t.get_job_display(),
        "image" : request.build_absolute_uri(t.image.url)
    } for t in titles]
    # print(request.build_absolute_uri())
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
        print("User not found")
        return HttpResponseForbidden()

    if data['unit'] == 'rose' and me.rose >= data['amount']:
        me.rose -= data['amount']
        me.save()
        him.rose += data['amount']
        him.save()
        print("Successfully transfered")
        return HttpResponse()
    elif data['unit'] == 'gear' and me.gear >= data['amount']:
        me.gear -= data['amount']
        me.save()
        him.gear += data['amount']
        him.save()
        print("Successfully transfered")
        return HttpResponse()
    else:
        print("Failed to transfer")
        return HttpResponseForbidden()


def rank_taker(request):
    """
    GET: show takers' rank
    """
    rank = User.objects.order_by('-gear')
    res = [{
        'name' : r.name,
        'title' : r.title_equipped.name if r.title_equipped is not None else "",
        'gear' : r.gear,
        'day' : (datetime.now().date() - r.reg_time).days,
        'image': r.image,
        'score': round(r.score_as_taker / r.times_as_taker, 5) if r.times_as_taker > 0 else 0
    } for r in rank]
    
    return JsonResponse(res, safe=False)


def rank_rider(request):
    """
    GET: show riders' rank
    """
    rank = User.objects.order_by('-rose')
    res = [{
        'name' : r.name,
        'title' : r.title_equipped.name if r.title_equipped is not None else "",
        'rose' : r.rose,
        'day' : (datetime.now().date() - r.reg_time).days,
        'image': r.image,
        'score': round(r.score_as_rider / r.times_as_rider, 5) if r.times_as_rider > 0 else 0
    } for r in rank]
    return JsonResponse(res, safe=False)