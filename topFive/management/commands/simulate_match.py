import random
import time
from django.core.management.base import BaseCommand
from topFive.models import Match


class Command(BaseCommand):
    help = 'Simulates the matches and updates the results'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting match simulation...')
        simulate_all_matches()
        self.stdout.write(self.style.SUCCESS('Successfully simulated all matches'))


def simulate_all_matches():
    matches = Match.objects.filter(completed=False)  # Get all incomplete matches
    for match in matches:
        simulate_game(match)


def simulate_game(match):
    home_team = match.home_team
    away_team = match.away_team

    stats = {
        'home_three_pointers': 0,
        'away_three_pointers': 0,
        'home_two_pointers': 0,
        'away_two_pointers': 0,
        'home_free_throws': 0,
        'away_free_throws': 0
    }

    outcomes = ['score', 'steal', 'turnover', 'block', 'miss_rebound_offense', 'miss_rebound_defense']

    def calculate_shot_success(player, shot_type):
        success_rate = {
            'three': player.shooting3 / 100.0,
            'two': player.shooting2 / 100.0,
            'free_throw': player.shooting2 / 100.0
        }
        return random.random() < success_rate.get(shot_type, 0)

    def handle_rebound(shot_missed, defending_player):
        if shot_missed:
            if random.random() < (defending_player.defense / 100.0):
                return 'block'
            return random.choice(['offensive_rebound', 'defensive_rebound'])
        return None

    def simulate_possession(attacking_team, defending_team):
        attacking_player = random.choice(list(attacking_team.players.all()))
        shot_type = random.choice(['three', 'two', 'free_throw'])
        shot_successful = calculate_shot_success(attacking_player, shot_type)

        if shot_successful:
            if attacking_team == home_team:
                if shot_type == 'three':
                    stats['home_three_pointers'] += 1
                elif shot_type == 'two':
                    stats['home_two_pointers'] += 1
                elif shot_type == 'free_throw':
                    stats['home_free_throws'] += 1
            else:
                if shot_type == 'three':
                    stats['away_three_pointers'] += 1
                elif shot_type == 'two':
                    stats['away_two_pointers'] += 1
                elif shot_type == 'free_throw':
                    stats['away_free_throws'] += 1
        else:
            handle_rebound(shot_missed=True, defending_player=random.choice(list(defending_team.players.all())))

    def play_quarter():
        for _ in range(60):  # Simulate 60 seconds per quarter
            simulate_possession(home_team, away_team)
            simulate_possession(away_team, home_team)
            time.sleep(1)  # Wait 1 second between each possession

    quarter = 1
    while quarter <= 4 or match.home_team_score == match.away_team_score:
        if quarter <= 4:
            print(f"Starting Quarter {quarter}...")
        else:
            print("Starting Overtime...")

        play_quarter()

        # Update scores after the quarter or overtime period
        match.home_team_score = stats['home_three_pointers'] * 3 + stats['home_two_pointers'] * 2 + stats[
            'home_free_throws']
        match.away_team_score = stats['away_three_pointers'] * 3 + stats['away_two_pointers'] * 2 + stats[
            'away_free_throws']

        quarter += 1

    match.completed = True
    match.result = "draw" if match.home_team_score == match.away_team_score else "win"
    match.save()
