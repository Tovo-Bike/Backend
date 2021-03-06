from django.shortcuts import render
from django.contrib.auth import hashers
from django.http.response import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from .models import Trip, Location
from users.models import User
from decimal import Decimal
import json
import math

# ===========================================================
# =                     Helper function                     =
# ===========================================================

def distance_on_sphere(lat1, long1, lat2, long2):
    """
    Convert latitude and longitude to spherical coordinates in radians.
    """
    degrees_to_radians = math.pi/180.0
    
    # phi = 90 - latitude
    phi1 = (90.0 - float(lat1))*degrees_to_radians
    phi2 = (90.0 - float(lat2))*degrees_to_radians
    
    # theta = longitude
    theta1 = float(long1)*degrees_to_radians
    theta2 = float(long2)*degrees_to_radians
    
    # Compute spherical distance from spherical coordinates.
    
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
    math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return round(arc * 6373 / 10 * 60)


def lanuch(request):
    """
    POST: A rider launches a new trip

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
    print("Successfully launched")
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
            'score' : round(a.rider.score_as_rider / a.rider.times_as_rider, 1) \
                        if a.rider.times_as_rider > 0 else 0,
            'weight': a.rider.weight, 
            'image' : a.rider.image,
            'slon': a.depart_lon,
            'slat': a.depart_lat,
            'elon': a.dest_lon,
            'elat': a.dest_lat,
            'duraton': distance_on_sphere(a.depart_lat, a.depart_lon, a.dest_lat, a.dest_lon) 
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
    taker.times_as_taker += 1
    taker.save()
    rider = trip.rider
    rider.times_as_rider += 1
    rider.rose += 1
    rider.save()
    print("Trip ended")
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