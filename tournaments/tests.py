from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tournament, Participant, Player, Round
from .serializers import ParticipantSerializer, TournamentSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        self.user = User.objects.create_user('user', 'user@example.com', 'password123')
        self.player = Player.objects.create(user=self.user)
        self.tournament = Tournament.objects.create(name='Test Tournament', num_of_rounds=3, start_date="2024-07-10", end_date="2024-08-11")
        self.participant = Participant.objects.create(player=self.player, tournament=self.tournament)
        self.tournament_participant_url = reverse('tournament-participants', kwargs={'pk': self.tournament.pk})
        self.participant_create_url = reverse('participant-create')
        self.participant_detail_url = reverse('participant-detail', kwargs={'pk': self.participant.pk})

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


class TournamentViewSetTests(BaseTestCase):
    def test_create_tournament(self):
        self.authenticate(self.admin_user)
        data = {
            "name": "New Tournament",
            "num_of_rounds": 5,
            "start_date": "2024-07-10",
            "end_date": "2024-08-10"
        }
        response = self.client.post(reverse('tournament-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tournament.objects.count(), 2)

    def test_list_tournaments(self):
        self.authenticate(self.admin_user)
        response = self.client.get(reverse('tournament-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class ParticipantViewSetTests(BaseTestCase):
    def test_create_participant(self):
        self.authenticate(self.admin_user)
        data = {
            "player_id": self.player.id,
            "tournament_id": self.tournament.id,
            "score": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }
        response = self.client.post(self.participant_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Participant.objects.count(), 2)

    def test_retrieve_participant(self):
        self.authenticate(self.admin_user)
        response = self.client.get(self.participant_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.participant.id)

class TournamentParticipantsListViewTests(BaseTestCase):
    def test_list_tournament_participants(self):
        self.authenticate(self.user)
        response = self.client.get(self.tournament_participant_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class TournamentSerializerTests(BaseTestCase):
    def test_create_tournament_serializer(self):
        data = {
            "name": "New Tournament",
            "num_of_rounds": 3,
            "start_date":"2024-07-10", 
            "end_date":"2024-08-11"
        }
        serializer = TournamentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tournament = serializer.save()
        self.assertEqual(tournament.name, "New Tournament")

    def test_update_tournament_serializer(self):
        tournament = Tournament.objects.create(name="Old Name", num_of_rounds=2, start_date="2024-07-10", end_date="2024-08-11")
        data = {
            "name": "Updated Name",
            "num_of_rounds": 3
        }
        serializer = TournamentSerializer(instance=tournament, data=data)
        self.assertTrue(serializer.is_valid())
        updated_tournament = serializer.save()
        self.assertEqual(updated_tournament.name, "Updated Name")
        self.assertEqual(updated_tournament.num_of_rounds, 3)

class ParticipantSerializerTests(BaseTestCase):
    def test_create_participant_serializer(self):
        data = {
            "player_id": self.player.id,
            "tournament_id": self.tournament.id,
            "score": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }
        serializer = ParticipantSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        participant = serializer.save()
        self.assertEqual(participant.player, self.player)
        self.assertEqual(participant.tournament, self.tournament)

    def test_update_participant_serializer(self):
        data = {
            "score": 10,
            "wins": 5,
            "draws": 3,
            "losses": 2
        }
        serializer = ParticipantSerializer(instance=self.participant, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_participant = serializer.save()
        self.assertEqual(updated_participant.score, 10)
        self.assertEqual(updated_participant.wins, 5)
        self.assertEqual(updated_participant.draws, 3)
        self.assertEqual(updated_participant.losses, 2)