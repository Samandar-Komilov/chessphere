class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.score = 0
        self.opponents = []

    def __str__(self):
        return self.name

class Match:
    def __init__(self, player1, player2, result):
        self.player1 = player1
        self.player2 = player2
        self.result = result  # 1 if player1 wins, 0 if draw, -1 if player2 wins

class Tournament:
    def __init__(self, players):
        self.players = players
        self.rounds = []

    def add_round(self, matches):
        self.rounds.append(matches)
        self.update_scores(matches)

    def update_scores(self, matches):
        for match in matches:
            p1, p2 = match.player1, match.player2
            if match.result == 1:
                p1.score += 1
            elif match.result == -1:
                p2.score += 1
            else:
                p1.score += 0.5
                p2.score += 0.5
            p1.opponents.append(p2.id)
            p2.opponents.append(p1.id)

    def get_leaderboard(self):
        return sorted(self.players, key=lambda p: (-p.score, p.name))


# Pairing Logic

def pair_players(players):
    players.sort(key=lambda p: (-p.score, p.name))
    pairs = []
    used = set()
    for i in range(len(players)):
        if players[i].id in used:
            continue
        for j in range(i+1, len(players)):
            if players[j].id in used or players[j].id in players[i].opponents:
                continue
            pairs.append((players[i], players[j]))
            used.add(players[i].id)
            used.add(players[j].id)
            break
    return pairs


def print_leaderboard(tournament):
    leaderboard = tournament.get_leaderboard()
    for rank, player in enumerate(leaderboard, start=1):
        print(f"{rank}. {player.name} - {player.score} points")


import random

# Create players
players = [Player(id=i, name=f"Player {i}") for i in range(20)]

# Initialize the tournament
tournament = Tournament(players)

# Simulate multiple rounds
num_rounds = 7
for round_num in range(1, num_rounds + 1):
    print(f"\nRound {round_num}")
    pairs = pair_players(tournament.players)
    print("Pairs:")
    for player1, player2 in pairs:
        print(f"{player1.name} vs {player2.name}")
    matches = []
    for player1, player2 in pairs:
        # Simulate a match result
        result = random.choice([1, 0, -1])
        matches.append(Match(player1, player2, result))
    tournament.add_round(matches)
    print_leaderboard(tournament)
