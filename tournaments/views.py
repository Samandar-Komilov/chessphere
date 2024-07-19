from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .models import Tournament, Round
from .serializers import (
    TournamentSerializer
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





""" A single ViewSet is used instead of 5 individual classes:


class TournamentsListView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    pagination_class = TournamentPagination


class AddTournamentView(generics.CreateAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]


class RetrieveTournamentView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    lookup_field = 'pk'


class UpdateTournamentView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    lookup_field = 'pk'


class DeleteTournamentView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    lookup_field = 'pk'

"""