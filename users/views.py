from django.shortcuts import render
from django.contrib.auth import hashers
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .models import User
from trips.models import Trip
import json


def show_all(request):
    """
    POST: show all users except the user itself

    Params: uid
    """
    data = json.loads(request.body)
    uid = data['uid']
    users = User.objects.exclude(id=uid)
    res = [{
        'uid': u.id,
        'name': u.name,
    } for u in users]
    return JsonResponse(res, safe=False)


def show_history(request):
    """
    POST: show a user's historical trips

    Params: uid
    """
    data = json.loads(request.body)
    uid = data['uid']
    his = Trip.objects.filter(
        Q(taker_id=uid) | Q(rider_id=uid),
        taker__isnull=False,
        start_time__isnull=False,
        arrival_time__isnull=False,
    )
    res = [{
        'tid': h.id,
        'taker': h.taker.name,
        'rider': h.rider.name,
        'taker_score': h.taker_score,
        'rider_score': h.rider_score,
        'start_time': h.start_time,
        'end_time': h.arrival_time,
        'duratoin': round((h.arrival_time - h.start_time).seconds / 60)
    } for h in his]
    print("Show history")
    return JsonResponse(res, safe=False)


def show_profile(request):
    """
    POST: A user require its profile
    """
    data = json.loads(request.body)
    print(">>>>>>>>> uid", data['uid'])
    user = User.objects.get(id=data['uid'])
    
    res = {
        'name': user.name,
        'email': user.email,
        'weight': user.weight,
        'gender': user.gender,
        'title_equipped': { 
            "ttid": user.title_equipped.id,
            "name": user.title_equipped.name 
        } if user.title_equipped is not None else "",
        'titles_had': [ { 
            "ttid": t.id, 
            "name": t.name 
            } for t in user.titles_had.all() ],
        'image': user.image,
        'score_as_taker': round(user.score_as_taker / user.times_as_taker) \
                            if user.times_as_taker > 0 else 0,
        'score_as_rider': round(user.score_as_rider / user.times_as_rider) \
                            if user.times_as_rider > 0 else 0,
        'gear': user.gear,
        'rose': user.rose,
    }
    return JsonResponse(res)

def update(request):
    """
    POST: update user profile
    """
    data = json.loads(request.body)
    user = User.objects.get(id=data['uid'])
    user.name = data['name']
    user.email = data['email']
    user.weight = data['weight']
    user.gender = data['gender']

    user.save()
    print("Successfully updated weight")
    return HttpResponse()


def create(request):
    """
    POST: A user registers

    Args:
        request.email
        request.name
        request.password
        request.gender
    """
    data = json.loads(request.body)
    name = data['name']
    if User.objects.filter(name=name).exists():
        print("User exists")
        return HttpResponseForbidden()
    password = hashers.make_password(data['password'])
    user = User(name=name, password=password,
                email=data['email'], gender=data['gender'])
    user.save()
    print("Successfully created")
    return HttpResponse()


def login(request):
    """
    POST: A user logs in

    Args:
        request.name
        request.password
    """
    data = json.loads(request.body)
    try:
        user = User.objects.get(name=data['name'])
    except ObjectDoesNotExist:
        print("User not found")
        return HttpResponseForbidden()

    if hashers.check_password(data['password'], user.password):
        return JsonResponse({'uid': user.id, 'name': user.name})
    else:
        print("Wrong password")
        return HttpResponseForbidden()

