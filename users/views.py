from django.shortcuts import render
from django.contrib.auth import hashers
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .models import User
from trips.models import Trip
import json

def show_history(request, uid):
    """
    GET: show a user's historical trips
    """ 
    his = Trip.objects.filter(Q(taker__id=uid) | Q(rider__id=uid)).exclude(arrival_time__isnull=True)
    res = [{
        'taker' : h.taker.name,
        'rider' : h.rider.name,
        'taker_score' : h.taker_score,
        'rider_score' : h.rider_score,
        'start_time' : h.start_time,
        'end_time' : h.arrival_time,
        'duratoin' : round((h.arrival_time - h.start_time).seconds / 60)
        } for h in his]
    return JsonResponse(res, safe=False)


def create(request):
    """
    POST: A user registers
    
    Args:
        request.email
        request.name
        request.password
    """
    data = json.loads(request.body)
    email = data['email']
    name = data['name']
    if User.objects.filter(name=name).exists():
        return HttpResponseForbidden("User exists")
    password = hashers.make_password(data['password'])
    user = User(name=name, password=password, email=email)
    user.save()
    return HttpResponse("Successfully created")


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
        return HttpResponseForbidden("User not found")

    if hashers.check_password(data['password'], user.password):
        return JsonResponse({'uid': user.id, 'name': user.name})
    else:
        return HttpResponseForbidden("Wrong password ")


def update(request):
    """
    POST: A user sets its profile
    
    Args:
        request.uid
        request.weight
    """
    data = json.loads(request.body)
    user = User.objects.get(id=data['uid'])
    user.weight = data['weight']
    user.save()
    return HttpResponse("Successfully updated")