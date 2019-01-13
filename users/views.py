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
    GET: show all users except the user itself

    Params: uid
    """
    data = json.load(request.body)
    uid = data['uid']
    users = User.objects.exclude(id=uid)
    res = [{
        'uid': u.id,
        'name': u.name,
    } for u in users]
    return JsonResponse(res, safe=False)


def show_history(request):
    """
    GET: show a user's historical trips

    Params: uid
    """
    data = json.load(request.body)
    uid = data['uid']
    his = Trip.objects.filter(Q(taker__id=uid) | Q(
        rider__id=uid)).exclude(arrival_time__isnull=True)
    res = [{
        'taker': h.taker.name,
        'rider': h.rider.name,
        'taker_score': h.taker_score,
        'rider_score': h.rider_score,
        'start_time': h.start_time,
        'end_time': h.arrival_time,
        'duratoin': round((h.arrival_time - h.start_time).seconds / 60)
    } for h in his]
    return JsonResponse(res, safe=False)


def show_profile(request, uid):
    """
    GET: A user require its profile
    """
    user = User.objects.get('uid')
    res = {
        'name': user.name,
        'email': user.email,
        'weight': user.weight,
        'score_as_taker': round(user.score_as_taker / user.times_as_taker) \
                            if user.times_as_taker > 0 else 0,
        'score_as_rider': round(user.score_as_rider / user.times_as_rider) \
                            if user.times_as_rider > 0 else 0,
        'gear': user.gear,
        'rose': user.rose,
    }
    return JsonResponse(res)


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


def set_weight(request):
    """
    POST: A user sets its weight

    Args:
        request.uid
        request.weight
    """
    data = json.loads(request.body)
    user = User.objects.get(id=data['uid'])
    user.weight = data['weight']
    user.save()
    print("Successfully updated weight")
    return HttpResponse()


def set_profile(request):
    """
    POST: A user sets its profile

    Args:
        request.uid
        request.image
    """
    data = json.loads(request.body)
    user = User.objects.get(id=data['uid'])
    user.image = data['image']
    user.save()
    print("Successfullt updated profile")
    return HttpResponse()
