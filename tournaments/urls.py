"""
URL Configuration for the Tournament application.

This module sets up the URL routing for the Tournament application using Django Rest Framework's DefaultRouter.
It registers the TournamentViewSet with the router to automatically generate the appropriate URLs for CRUD operations.

Routes:
    - /tournaments/: Handles all operations (list, create, retrieve, update, delete) for Tournament instances.

Modules:
    - django.urls: Provides functions to define URL patterns.
    - rest_framework.routers: Provides a router for automatic URL routing with DRF viewsets.
    - .views: Imports the TournamentViewSet which contains the logic for handling tournament-related requests.

Usage:
    Include this URL configuration in the project's main urls.py file to enable the routes:
        path('api/', include('tournament.urls'))
"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TournamentViewSet


router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)


urlpatterns = [
    path('', include(router.urls))
]