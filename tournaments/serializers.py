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
    """
    Serializer for Participant model to represent tournament participants.

    This serializer is used to serialize and deserialize the data of participants in a tournament.
    It includes the nested player data and other participant details.

    Attributes:
        player (PlayerSerializer): Nested serializer for player data, read-only.

    Meta:
        model (Model): The model class that is being serialized.
        fields (list): The list of fields to be included in the serialized representation.
    """
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'player', 'score', 'wins', 'draws', 'losses']



class ParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Participant model.

    This serializer is used to create and update Participant instances. It includes additional validation
    to ensure a player does not participate in a tournament more than once.

    Attributes:
        player_id (IntegerField): The ID of the player participating in the tournament, defaults to 1.
        tournament_id (IntegerField): The ID of the tournament, defaults to 1.

    Meta:
        model (Model): The model class that is being serialized.
        fields (list): The list of fields to be included in the serialized representation.
    
    Methods:
        create(validated_data):
            Creates a new Participant instance after validating the player and tournament data.
        
        update(instance, validated_data):
            Updates an existing Participant instance, ensuring 'player_id' and 'tournament_id' cannot be changed.
    """
    player_id = serializers.IntegerField(default=1)
    tournament_id = serializers.IntegerField(default=1)

    class Meta:
        model = Participant
        fields = ['id', 'player_id', 'tournament_id', 'score', 'wins', 'draws', 'losses']

    def create(self, validated_data):
        """
        Create a new Participant instance.

        Validates that a player does not participate in the same tournament more than once. 
        Removes 'player_id' and 'tournament_id' from validated data after fetching the corresponding objects.

        Args:
            validated_data (dict): The validated data for creating a new Participant instance.

        Returns:
            Participant: The created Participant instance.

        Raises:
            ValidationError: If the player is already participating in the tournament.
        """
        player_id = validated_data.get('player_id')
        tournament_id = validated_data.get('tournament_id')

        player_ids = [participant.player_id for participant in Participant.objects.filter(tournament_id=tournament_id)]
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
        """
        Update an existing Participant instance.

        Ensures 'player_id' and 'tournament_id' cannot be changed once the participant has been created.
        Updates the participant's score, wins, draws, and losses.

        Args:
            instance (Participant): The existing Participant instance to be updated.
            validated_data (dict): The validated data for updating the Participant instance.

        Returns:
            Participant: The updated Participant instance.

        Raises:
            ValidationError: If 'player_id' or 'tournament_id' are included in the validated data.
        """
        if 'player_id' in validated_data:
            raise ValidationError("Cannot update 'player' once the participant has been created.")
        if 'tournament_id' in validated_data:
            raise ValidationError("Cannot update 'tournament' once the participant has been created.")
        

        instance.score = validated_data.get('score', instance.score)
        instance.wins = validated_data.get('wins', instance.wins)
        instance.draws = validated_data.get('draws', instance.draws)
        instance.losses = validated_data.get('losses', instance.losses)
        instance.save()

        return instance