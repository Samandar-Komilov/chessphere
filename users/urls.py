from django.urls import path
from .views import (
    Home, 
    RegisterView,
    PlayersListView,
    AddPlayerView,
    ReadPlayerView,
    UpdatePlayerView,
    DeletePlayerView,
    PlayerChangeActivityView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


urlpatterns = [
    path('', Home.as_view(), name='home'),

    # auth
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # player management
    path('players/', PlayersListView.as_view(), name='players-list'),
    path('players/add/', AddPlayerView.as_view(), name='add-player'),
    path('players/<int:pk>/', ReadPlayerView.as_view(), name='read-player'),
    path('players/update/<int:pk>/', UpdatePlayerView.as_view(), name='update-player'),
    path('players/delete/<int:pk>/', DeletePlayerView.as_view(), name='delete-player'),
    path('players/activity/<int:pk>/', PlayerChangeActivityView.as_view(), name='change-player-activity'),
]
