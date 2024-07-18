from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Player


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        Player.objects.create(user=user)

        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined']


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model.

    This serializer handles the serialization and deserialization of Player objects.
    It includes nested serialization for the related User object and provides
    validation and creation methods for the Player model.

    Fields:
        user (User): The related User object.
        country (str): The country of the player.
        first_name (str): The first name of the player.
        age (int): The age of the player.
    """

    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['id', 'user', 'country', 'birthdate', 'rating']

    def create(self, validated_data):
        """
        Create method to handle nested creation of the Player model.

        This method creates a new User instance and associates it with the Player instance.

        Args:
            validated_data (dict): The validated data containing the information for the Player.

        Returns:
            Player: The created Player instance.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)

        player = Player.objects.create(user=user, **validated_data)
        return player

    def update(self, instance, validated_data):
        """
        Update method to handle nested updates for the Player model.

        This method updates the Player instance and its related User instance.
        It ensures that changes to user-related fields are handled appropriately.

        Args:
            instance (Player): The Player instance to be updated.
            validated_data (dict): The validated data containing updates for the Player.

        Returns:
            Player: The updated Player instance.
        """
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update Player fields
        instance.country = validated_data.get('country', instance.country)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()

        # Update User fields
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return instance
