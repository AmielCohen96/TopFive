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

    # Initialize scores and stats
    stats = {
        'home_three_pointers': 0,
        'away_three_pointers': 0,
        'home_two_pointers': 0,
        'away_two_pointers': 0,
        'home_free_throws': 0,
        'away_free_throws': 0
    }

    # Define possible outcomes
    outcomes = {
        'score': 0,
        'steal': 1,
        'turnover': 2,
        'block': 3,
        'miss_rebound_offense': 4,
        'miss_rebound_defense': 5
    }

    def calculate_shot_success(player, shot_type):
        """Calculate if a shot is successful based on shot type and player stats"""
        success_rate = {
            'three': player.shooting3 / 100.0,
            'two': player.shooting2 / 100.0,
            'free_throw': player.shooting2 / 100.0
        }
        return random.random() < success_rate.get(shot_type, 0)

    def handle_rebound(shot_missed, defending_player):
        """Determine the result of a missed shot, including possible rebounds"""
        if shot_missed:
            if random.random() < (defending_player.defense / 100.0):
                return 'block'
            return random.choice(['offensive_rebound', 'defensive_rebound'])
        return None

    def simulate_possession(attacking_team, defending_team):
        """Simulate a single possession for an attacking team against a defending team"""
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
            rebound_result = handle_rebound(shot_missed=True,
                                            defending_player=random.choice(list(defending_team.players.all())))
            return rebound_result

    # Simulate the game over the course of 1 minute
    for _ in range(60):  # Simulate for 60 seconds
        simulate_possession(home_team, away_team)
        simulate_possession(away_team, home_team)
        time.sleep(1)  # Wait 1 second between each possession

    # Update the match with the simulated stats
    match.update_scores(
        home_three_pointers=stats['home_three_pointers'],
        away_three_pointers=stats['away_three_pointers'],
        home_two_pointers=stats['home_two_pointers'],
        away_two_pointers=stats['away_two_pointers'],
        home_free_throws=stats['home_free_throws'],
        away_free_throws=stats['away_free_throws']
    )

