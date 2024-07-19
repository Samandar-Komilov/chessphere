from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Tournament, Round

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
