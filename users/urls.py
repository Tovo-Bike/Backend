from django.urls import path, include
from users import views

# user/...
urlpatterns = [
    path('<int:uid>', views.show_history),
    path('create', views.create),
    path('login', views.login),
    path('set', views.update),
]
