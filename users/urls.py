from django.urls import path
from .views import (
    RegisterView,
    PlayersListView,
    AddPlayerView,
    ReadPlayerView,
    UpdatePlayerView,
    DeletePlayerView,
    PlayerChangeActivityView,
    ProfileUpdateView,
    ProfileView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Player management
    path('players/', PlayersListView.as_view(), name='players-list'),
    path('players/add/', AddPlayerView.as_view(), name='add-player'),
    path('players/<int:pk>/', ReadPlayerView.as_view(), name='read-player'),
    path('players/update/<int:pk>/', UpdatePlayerView.as_view(), name='update-player'),
    path('players/delete/<int:pk>/', DeletePlayerView.as_view(), name='delete-player'),
    path('players/activity/<int:pk>/', PlayerChangeActivityView.as_view(), name='change-player-activity'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit')
]

"""
URL Patterns:

Authentication endpoints:
- 'register/': Register a new user.
- 'token/': Obtain JWT tokens (Log In).
- 'token/refresh/': Refresh JWT tokens.
- 'token/verify/': Verify JWT tokens.
- 'token/blacklist/': Blacklist JWT tokens (Log Out).

Player management endpoints:
- 'players/': List all players (admin only).
- 'players/add/': Add a new player (admin only).
- 'players/<int:pk>/': Read details of a specific player (admin only).
- 'players/update/<int:pk>/': Update details of a specific player (admin only).
- 'players/delete/<int:pk>/': Delete a specific player (admin only).
- 'players/activity/<int:pk>/': Change the activity status of a specific player (admin only).

Profile endpoints:
- 'profile/': View the profile of the logged-in user.
- 'profile/edit/': Edit the profile of the logged-in user.
"""