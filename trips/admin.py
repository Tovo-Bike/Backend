from django.contrib import admin
from .models import Trip, Location, Report

admin.site.register(Location)
admin.site.register(Trip)
admin.site.register(Report)