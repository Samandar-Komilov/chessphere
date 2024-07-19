from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

from users.models import Player

from faker import Faker

faker = Faker()


class Tournament(models.Model):
    name = models.CharField(max_length=100, default=f"{faker.name()}'s Cup", blank=False, null=False)
    start_date = models.DateField(default=datetime.utcnow().strftime("%Y-%M-%d"))
    end_date = models.DateField(default=datetime.utcnow().strftime("%Y-%M-%d"))
    num_of_rounds = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(11)], default=1, blank=False, null=False)

    def __str__(self):
        return f"Tournament: {self.name}, Rounds: {self.num_of_rounds}"


class Participant(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
    score = models.FloatField(default=0, blank=False, null=False)
    wins = models.IntegerField(default=0, blank=False, null=False)
    draws = models.IntegerField(default=0, blank=False, null=False)
    losses = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"
    

class Round(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.IntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return f"Round {self.round_number} - {self.tournament.name}"
    

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    white = models.ForeignKey(Participant, related_name='white_matches', on_delete=models.CASCADE)
    black = models.ForeignKey(Participant, related_name='black_matches', on_delete=models.CASCADE)
    winner = models.ForeignKey(Participant, related_name='won_matches', on_delete=models.CASCADE)
    draw = models.BooleanField(default=False, blank=False, null=False)
    duration = models.DurationField(blank=True)
    played_at = models.DateTimeField(auto_now=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.draw:
            self.first_participant.score += 0.5
            self.second_participant.score += 0.5
            self.first_participant.save()
            self.second_participant.save()
        elif self.winner:
            self.winner.score += 1
            self.winner.save()

    def __str__(self):
        return f"{self.white} vs {self.black} - {self.tournament.name}"