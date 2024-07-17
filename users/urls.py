from django.urls import path
from .views import Home, RegisterView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register')
]
