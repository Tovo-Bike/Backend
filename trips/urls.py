from django.urls import path
from trips import views

# trip/...
urlpatterns = [
    path('go', views.lanuch),
    path('', views.find),
    path('accept', views.accept),
    path('start', views.start),
    path('end', views.end),
    path('rate', views.rate),
]