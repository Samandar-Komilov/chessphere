import random
from django.utils import timezone
from .models import Tournament, Match, Participant, Round


def generate_swiss_pairings(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    participants = list(tournament.participants.order_by('-score'))
    num_of_rounds = tournament.num_of_rounds
    i = 1

    while i<num_of_rounds+1:
        if len(participants)<2:
            break
        white = participants.pop(0)
        black = participants.pop(0)

        result = random.choice([-1, 0, 1])

        if result == 0:
            winner = None
            draw = True
        elif result == -1:
            winner = white
            draw = False
        else:
            winner = black
            draw = False

        current_round = Round.objects.get(tournament=tournament, round_number=i)
        print(current_round)

        Match.objects.create(
            tournament = tournament,
            round = current_round,
            white = white,
            black = black,
            winner = winner,
            draw = draw,
            played_at = timezone.now()
        )

        white.save()
        black.save()

        i+=1