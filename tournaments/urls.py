"""
URL configuration for the tournament and participant views.

This module sets up the routing of URLs to the appropriate viewsets and views.
It uses Django REST Framework's DefaultRouter to handle the routing for the TournamentViewSet.
Additional paths are defined for listing participants of a specific tournament and for creating, retrieving, updating, and deleting participants.

Routes:
    - '' (root): Includes all routes registered with the DefaultRouter.
    - 'tournaments/<int:pk>/participants/': Lists all participants for a specific tournament (specified by ID).
    - 'participants/create/': Creates a new participant.
    - 'participants/<int:pk>/': Retrieves, updates, partially updates, or deletes a specific participant (specified by ID).

Attributes:
    router (DefaultRouter): The router instance used to register the TournamentViewSet routes.
    urlpatterns (list): The list of URL patterns for routing requests to the appropriate views.
"""


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TournamentViewSet, ParticipantViewSet, TournamentParticipantsListView


router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)


urlpatterns = [
    # Tournaments
    path('', include(router.urls)),
    path('tournaments/<int:pk>/participants/', TournamentParticipantsListView.as_view(), name="tournament-participants"),

    # Participants
    path('participants/create/', ParticipantViewSet.as_view({'post': 'create'}), name='participant-create'),
    path('participants/<int:pk>/', ParticipantViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='participant-detail'),
    # path('participants', ParticipantViewSet.as_view({'get': 'list'}), name='participant-list'),
]