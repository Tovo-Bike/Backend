from django.urls import path, include
from users import views

# user/...
urlpatterns = [
    path('profile', views.show_profile),
    path('his', views.show_history),
    path('all', views.show_all),
    path('create', views.create),
    path('login', views.login),
    path('update', views.update),
]
