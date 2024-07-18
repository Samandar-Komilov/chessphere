from django.db import models
from users.models import Player


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    

class Participant(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, related_name='participants', on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"
    

class Round(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='rounds', on_delete=models.CASCADE)
    round_number = models.IntegerField()

    def __str__(self):
        return f"Round {self.round_number} - {self.tournament.name}"
    

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    white = models.ForeignKey(Participant, related_name='white_matches', on_delete=models.CASCADE)
    black = models.ForeignKey(Participant, related_name='black_matches', on_delete=models.CASCADE)
    winner = models.ForeignKey(Participant, related_name='won_matches', on_delete=models.CASCADE)
    draw = models.BooleanField(default=False)
    duration = models.DurationField()
    played_at = models.DateTimeField(auto_now=True)

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