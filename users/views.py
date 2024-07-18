from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Player
from .serializers import (
    RegisterSerializer, 
    UserSerializer,
    PlayerSerializer
)


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {"message": "Hello World!"}
        return Response(content)
    

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })
    

# CRUD operations on Players by admin users


class PlayerPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 50


class PlayersListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    pagination_class = PlayerPagination


class AddPlayerView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer


class ReadPlayerView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    lookup_field = 'pk'


class UpdatePlayerView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    lookup_field = 'pk'


class DeletePlayerView(generics.DestroyAPIView):
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