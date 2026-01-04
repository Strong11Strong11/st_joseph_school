from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_view, name='about'),
    path('team/', views.team_view, name='team'),
]