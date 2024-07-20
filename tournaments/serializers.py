from rest_framework import serializers
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import Tournament, Round, Participant, Match, Player
from users.serializers import PlayerSerializer

class TournamentSerializer(serializers.ModelSerializer):
    """
    TournamentSerializer handles serialization and deserialization of Tournament instances.
    It ensures that the 'num_of_rounds' field cannot be updated once rounds have been created.

    Meta:
        model (Tournament): The Tournament model.
        fields (list): The fields to be included in the serialized data.
    """

    class Meta:
        model = Tournament
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Tournament instance along with the specified number of rounds.

        Args:
            validated_data (dict): The validated data used to create the Tournament instance.

        Returns:
            Tournament: The newly created Tournament instance.
        """
        tournament = Tournament.objects.create(**validated_data)
        # Create rounds as well
        num_of_rounds = tournament.num_of_rounds
        for i in range(1, num_of_rounds+1):
            Round.objects.create(tournament=tournament, round_number=i)
        return tournament
    
    def update(self, instance, validated_data):
        """
        Updates a Tournament instance. Raises a validation error if 'num_of_rounds'
        is attempted to be updated and round objects have been created.

        Args:
            instance (Tournament): The Tournament instance to be updated.
            validated_data (dict): The validated data from the serializer.

        Returns:
            Tournament: The updated Tournament instance.

        Raises:
            ValidationError: If 'num_of_rounds' is attempted to be updated and rounds exist.
        """
        if 'num_of_rounds' in validated_data:
            if Round.objects.filter(tournament=instance).exists():
                raise ValidationError("Cannot update 'num_of_rounds' once rounds have been created.")
            else:
                # If the Round objects have not been created yet:
                instance.num_of_rounds = validated_data['num_of_rounds']

        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        return instance
    

class TournamentParticipantSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'player', 'score', 'wins', 'draws', 'losses']



class ParticipantSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(default=1)
    tournament_id = serializers.IntegerField(default=1)

    class Meta:
        model = Participant
        fields = ['id', 'player_id', 'tournament_id', 'score', 'wins', 'draws', 'losses']

    def create(self, validated_data):
        player_id = validated_data.get('player_id')
        tournament_id = validated_data.get('tournament_id')

        player_ids = [participant.player_id for participant in Participant.objects.filter(tournament_id=tournament_id)]
        print(player_id)
        print(player_ids)
        if player_id in player_ids:
            raise ValidationError("A single player cannot participate in a tournament twice!")
        else:
            player = Player.objects.get(id=player_id)
            tournament = Tournament.objects.get(id=tournament_id)

            validated_data.pop('player_id')
            validated_data.pop('tournament_id')

            participant = Participant.objects.create(
                player=player,
                tournament=tournament,
                **validated_data
            )

            return participant
    
    def update(self, instance, validated_data):
        if 'player_id' in validated_data:
            raise ValidationError("Cannot update 'player' once the participant has been created.")
        if 'tournament_id' in validated_data:
            raise ValidationError("Cannot update 'tournament' once the participant has been created.")
        

        instance.score = validated_data.get('score', instance.score)
        instance.wins = validated_data.get('wins', instance.wins)
        instance.draws = validated_data.get('draws', instance.draws)
        instance.losses = validated_data.get('losses', instance.losses)
        instance.save()