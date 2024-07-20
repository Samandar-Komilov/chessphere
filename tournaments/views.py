from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Tournament, Round, Participant, Match
from .serializers import (
    TournamentSerializer,
    ParticipantSerializer,
    TournamentParticipantSerializer
)


class TournamentPagination(PageNumberPagination):
    """
    TournamentPagination handles pagination for the Tournament list view.

    Attributes:
    - page_size_query_param: The query parameter name for the page size.
    - page_size: The default number of items per page.
    - max_page_size: The maximum number of items per page.
    """
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 50


class ParticipantPagination(PageNumberPagination):
    """
    ParticipantPagination handles pagination for the Participant list view.

    Attributes:
    - page_size_query_param: The query parameter name for the page size.
    - page_size: The default number of items per page.
    - max_page_size: The maximum number of items per page.
    """
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 50


class TournamentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing tournament instances.
    Provides 'list', 'create', 'retrieve', 'update', and 'destroy' actions.

    Attributes:
        queryset (QuerySet): The queryset that should be used for retrieving objects from the database.
        serializer_class (Serializer): The serializer class to be used for serializing and deserializing data.
        permission_classes (list): A list of permission classes that determines who can access this viewset.
        authentication_classes (list): A list of authentication classes to determine how the request should be authenticated.
        pagination_class (Pagination): The pagination class to paginate the response.

    Methods:
        perform_create(self, serializer): Handles the creation of a new tournament instance. It is called
            after the serializer has validated the incoming data. The method saves the serializer
            to create a new tournament in the database.

        perform_update(self, serializer): Handles the updating of an existing tournament instance. It is
            called after the serializer has validated the incoming data. The method saves the serializer
            to update the existing tournament in the database.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    pagination_class = TournamentPagination

    def perform_create(self, serializer):
        """Save the serializer to create a new tournament."""
        serializer.save()

    def perform_update(self, serializer):
        """Save the serializer to update an existing tournament."""
        serializer.save()


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    pagination_class = ParticipantPagination

    def perform_create(self, serializer):
        """Save the serializer to create a new participant."""
        serializer.save()

    def perform_update(self, serializer):
        """Save the serializer to update an existing participant."""
        serializer.save()


class TournamentParticipantsListView(generics.ListAPIView):
    serializer_class = TournamentParticipantSerializer
    pagination_class = ParticipantPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all participants for a tournament as specified by the tournament ID (pk) in the URL.
        """
        tournament_id = self.kwargs['pk']
        return Participant.objects.filter(tournament_id=tournament_id).select_related('player__user')
