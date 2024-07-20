from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Player


class UserRegistrationTest(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(response.data['user']['username'], 'testuser')


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        Player.objects.create(user=self.user)
    
    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_refresh_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']
        
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class PlayerCRUDTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.player_user = User.objects.create_user(username='player', password='playerpassword123')
        self.player = Player.objects.create(user=self.player_user, country='USA', birthdate='2000-01-01', rating=1000)
    
    def test_list_players(self):
        url = reverse('players-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_add_player(self):
        url = reverse('add-player')
        data = {
            'user': {
                'username': 'newplayer',
            },
            'country': 'UK',
            'birthdate': '2001-02-02',
            'rating': 1500
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(response.data['user']['username'], 'newplayer')
    
    def test_read_player(self):
        url = reverse('read-player', kwargs={'pk': self.player.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'player')
    
    def test_update_player(self):
        url = reverse('update-player', kwargs={'pk': self.player.pk})
        data = {
            'user': {
                'username': 'updatedplayer',
                "first_name": "Updated1",
                "last_name": "Updated1",
            },
            'country': 'UZ',
            'birthdate': '2002-03-03',
            'rating': 1200,
            
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player.refresh_from_db()
        self.assertEqual(self.player.country, 'UZ')
        self.assertEqual(self.player.user.username, 'updatedplayer')
        self.assertEqual(self.player.user.first_name, 'Updated1')
        self.assertEqual(self.player.user.last_name, 'Updated1')
    
    def test_delete_player(self):
        url = reverse('delete-player', kwargs={'pk': self.player.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 0)


class PlayerProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.player = Player.objects.create(user=self.user, country='USA', birthdate='2000-01-01', rating=1000)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_view_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['id']['username'], 'testuser')
    
    def test_update_profile(self):
        url = reverse('profile-edit')
        data = {
            'email': 'newemail@example.com',
            'country': 'UZ',
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'birthdate': '2002-03-03',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.player.refresh_from_db()
        self.assertEqual(self.player.country, 'UZ')
        self.assertEqual(self.player.user.email, 'newemail@example.com')
        self.assertEqual(self.player.user.first_name, 'NewFirstName')
        self.assertEqual(self.player.user.last_name, 'NewLastName')
