from django.urls import path, include
from users import views

# user/...
urlpatterns = [
    path('', views.show_history),
    path('all', views.show_all),
    path('create', views.create),
    path('login', views.login),
    path('set', views.update),
]
