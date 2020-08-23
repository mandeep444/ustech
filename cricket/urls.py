from django.urls import path, re_path

from cricket.views import *

urlpatterns = [
    path('', index, name='home'),
    path('teams/', teams, name='teams'),
    path('team/<slug>/', teams, name='team'),
    path('players/', players, name='players'),
    path('player/<slug>/', players, name='player'),
]