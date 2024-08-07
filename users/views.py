from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import User

from .models import Player
from .serializers import (
    RegisterSerializer, 
    UserSerializer,
    PlayerSerializer,
    ProfileUpdateSerializer
)
    

class RegisterView(generics.GenericAPIView):
    """
    RegisterView handles the user registration process.

    Methods:
    - post: Handles POST requests for user registration.

    Attributes:
    - serializer_class: Specifies the serializer to be used for registration.
    - permission_classes: Specifies that any user is allowed to access this view.
    - authentication_classes: Specifies the authentication mechanism (JWT).
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args,  **kwargs):
        """
        Handle POST requests to register a new user.

        Args:
        - request: The request object containing user registration data.

        Returns:
        - Response: A response containing the newly created user's data and a success message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)
    

# CRUD operations on Players by admin users


class PlayerPagination(PageNumberPagination):
    """
    PlayerPagination handles pagination for the Player list view.

    Attributes:
    - page_size_query_param: The query parameter name for the page size.
    - page_size: The default number of items per page.
    - max_page_size: The maximum number of items per page.
    """
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 50


class PlayersListView(generics.ListAPIView):
    """
    PlayersListView provides a list of all players. Only accessible by admin users.

    Attributes:
    - queryset: Specifies the queryset to be used (all Player objects).
    - serializer_class: Specifies the serializer to be used (PlayerSerializer).
    - permission_classes: Specifies that only authenticated admin users can access this view.
    - pagination_class: Specifies the pagination class to be used (PlayerPagination).
    """
    queryset = Player.objects.all().order_by('id')
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = PlayerPagination


class AddPlayerView(generics.CreateAPIView):
    """
    AddPlayerView handles the creation of new players. Only accessible by admin users.

    Attributes:
    - serializer_class: Specifies the serializer to be used (PlayerSerializer).
    - permission_classes: Specifies that only authenticated admin users can access this view.
    - authentication_classes: Specifies the authentication mechanism (JWT).
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer


class ReadPlayerView(generics.RetrieveAPIView):
    """
    ReadPlayerView provides details of a specific player. Only accessible by admin users.

    Attributes:
    - serializer_class: Specifies the serializer to be used (PlayerSerializer).
    - queryset: Specifies the queryset to be used (all Player objects).
    - permission_classes: Specifies that only authenticated admin users can access this view.
    - authentication_classes: Specifies the authentication mechanism (JWT).
    - lookup_field: Specifies the field to look up the player (default is 'pk').
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    lookup_field = 'pk'


class UpdatePlayerView(generics.UpdateAPIView):
    """
    UpdatePlayerView handles the update of existing player details. Only accessible by admin users.

    Attributes:
    - serializer_class: Specifies the serializer to be used (PlayerSerializer).
    - queryset: Specifies the queryset to be used (all Player objects).
    - permission_classes: Specifies that only authenticated admin users can access this view.
    - authentication_classes: Specifies the authentication mechanism (JWT).
    - lookup_field: Specifies the field to look up the player (default is 'pk').
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    lookup_field = 'pk'


class DeletePlayerView(generics.DestroyAPIView):
    """
    DeletePlayerView handles the deletion of players. Only accessible by admin users.

    Attributes:
    - serializer_class: Specifies the serializer to be used (PlayerSerializer).
    - queryset: Specifies the queryset to be used (all Player objects).
    - permission_classes: Specifies that only authenticated admin users can access this view.
    - authentication_classes: Specifies the authentication mechanism (JWT).
    - lookup_field: Specifies the field to look up the player (default is 'pk').
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    lookup_field = 'pk'


class PlayerChangeActivityView(APIView):
    """
    View to disable or enable a player by toggling the is_active field.
    Accessible only by admin users.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk, *args, **kwargs):
        """
        Toggle the is_active field of the player with the given primary key (pk).

        Args:
            request: The request object.
            pk (int): The primary key of the player to be toggled.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            Response: The response object indicating the result of the toggle operation.
        """
        try:
            player = Player.objects.get(pk=pk)
            user = player.user
            user.is_active = not user.is_active
            user.save()
            status_message = 'activated' if user.is_active else 'disabled'
            return Response({'status': f'Player has been {status_message}.'}, status=status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found.'}, status=status.HTTP_404_NOT_FOUND)
        


class ProfileView(generics.RetrieveAPIView):
    """
    View to retrieve a player's own profile details. Accessible by authenticated players.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        """
        Return the Player instance for the authenticated user.
        """
        user = User.objects.get(id=self.request.user.id)
        return Player.objects.get(user=user)

    def get(self, request, *args, **kwargs):
        """
        Handle retrieval of the player's own profile details.

        Args:
            request: The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The response object containing the player's profile details.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProfileUpdateView(generics.UpdateAPIView):
    """
    View to update a player's own details. Accessible by authenticated players.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileUpdateSerializer
    
    def get_object(self):
        """
        Return the Player instance for the authenticated user.
        """
        user = User.objects.get(id=self.request.user.id)
        return Player.objects.get(user=user)
    
    def get(self, request, *args, **kwargs):
        pass
    
    def update(self, request, *args, **kwargs):
        """
        Handle updates to a player's own profile details.
        
        Args:
            request: The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
            
        Returns:
            Response: The response object indicating the result of the update operation.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)