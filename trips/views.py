from django.shortcuts import render
from django.contrib.auth import hashers
from django.http.response import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from .models import Trip, Location
from users.models import User
import json


def lanuch(request):
    """
    POST: A user launches a new trip

    Args:
        request.uid
        request.slon
        request.slat
        request.elon
        request.elat
    """
    data = json.loads(request.body)
    trip = Trip(
        rider = User.objects.get(id=data['uid']),
        depart_lon = data['slon'],
        depart_lat = data['slat'],
        dest_lon = data['elon'],
        dest_lat = data['elat'],
    )
    trip.save()
    return JsonResponse({'tid': trip.id})


def find(request):
    """
    GET: A taker looks for new trips
    """
    available = Trip.objects.filter(taker__isnull=True)
    res = [
        {
            'tid': a.id,
            'name': a.rider.name,
            'gender' : a.rider.get_gender_display(),
            'score' : round(a.rider.score_as_rider / a.rose, 1) if a.rose > 0 else 0,
            'weight': a.rider.weight, 
            'slon': a.depart_lon,
            'slat': a.depart_lat,
            'elon': a.dest_lon,
            'elat': a.dest_lat,
        } for a in available]
    return JsonResponse(res, safe=False)
    
    
def accept(request):
    """
    POST: A taker accepts the trip

    Args:
        request.uid
        request.tid
    """
    data = json.loads(request.body)
    trip = Trip.objects.get(id=data['tid'])
    trip.taker = User.objects.get(id=data['uid'])
    trip.save()
    print("Successfully accepted")
    return HttpResponse()


def start(request):
    """
    POST: A trip starts

    Args:
        request.tid
    """
    data = json.loads(request.body)
    trip = Trip.objects.get(id=data['tid'])
    trip.start_time = timezone.now()
    trip.save()
    print("Trip started")
    return HttpResponse()


def end(request):
    """
    POST: A trip ends

    Args:
        request.tid
    """
    data = json.loads(request.body)
    trip = Trip.objects.get(id=data['tid'])
    trip.arrival_time = timezone.now()
    trip.save()
    dur = (trip.arrival_time - trip.start_time).seconds // 60

    taker = trip.taker
    taker.gear += 1
    taker.save()
    rider = trip.rider
    rider.rose += 1
    rider.save()
    return JsonResponse({'time': dur}) 


def rate(request):
    """
    POST: A user rate the trip

    Args:
        request.tid
        request.uid
        request.point
    """
    data = json.loads(request.body)
    trip = Trip.objects.get(id=data['tid'])
    user = User.objects.get(id=data['uid']) 
    if trip.taker.id == data['uid']:
        trip.rider_score = data['point']
        user.score_as_rider += data['point']
    else:
        trip.taker_score = data['point']
        user.score_as_taker += data['point']
    user.save()
    trip.save()
    print("Successfully rated")
    return HttpResponse()