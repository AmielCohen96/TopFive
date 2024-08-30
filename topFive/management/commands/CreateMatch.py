import datetime
import random
from datetime import timedelta

from django.core.management import BaseCommand

from topFive.models import Match, League


class Command(BaseCommand):
    help = 'Creates matches based on the league creation date'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating matches based on league creation dates...')
        create_matches()
        self.stdout.write(self.style.SUCCESS('Successfully created matches'))


def create_matches():
    leagues = League.objects.all().order_by('-id')  # Get all leagues

    for league in leagues:
        teams = list(league.teams.all())  # Get all teams in the league
        if not teams:
            continue

        num_teams = len(teams)
        total_rounds = (num_teams - 1) * 2  # Total rounds needed to play each team twice
        start_date = datetime.datetime.now() + timedelta(minutes=5)  # Start date for matches

        # Generate match dates
        match_dates = [start_date + timedelta(minutes=round_num * 5) for round_num in range(total_rounds)]

        # Helper function to generate the schedule for a given round
        def generate_round_robin_matches(teams, reverse_roles=False):
            round_matches = []
            num_teams = len(teams)
            random.shuffle(teams)  # Shuffle teams for randomness

            for i in range(0, num_teams, 2):
                if i + 1 < num_teams:
                    home_team = teams[i]
                    away_team = teams[i + 1]
                    if reverse_roles:
                        round_matches.append((away_team, home_team))  # Reverse roles
                    else:
                        round_matches.append((home_team, away_team))
            return round_matches

        # Generate matches for the first section
        first_section_matches = []
        for _ in range(num_teams - 1):
            round_matches = generate_round_robin_matches(teams)
            first_section_matches.append(round_matches)
            teams = teams[1:] + [teams[0]]  # Rotate teams

        # Generate matches for the second section with reversed roles
        second_section_matches = []
        for _ in range(num_teams - 1):
            round_matches = generate_round_robin_matches(teams, reverse_roles=True)
            second_section_matches.append(round_matches)
            teams = teams[1:] + [teams[0]]  # Rotate teams

        # Combine matches
        all_matches = first_section_matches + second_section_matches

        # Initialize the last match date for each team
        last_match_dates = {team: start_date - timedelta(days=7) for team in teams}
        match_date_index = 0

        # Schedule the matches
        for round_matches in all_matches:
            match_date = match_dates[match_date_index]
            for home_team, away_team in round_matches:
                # Ensure no team plays more than once per day
                while any(last_match_dates[team] == match_date for team in [home_team, away_team]):
                    match_date_index += 1
                    if match_date_index >= len(match_dates):
                        break
                    match_date = match_dates[match_date_index]

                if match_date_index >= len(match_dates):
                    break

                Match.objects.create(
                    home_team=home_team,
                    away_team=away_team,
                    match_date=match_date,
                    league=league
                )

                # Update the last match dates
                last_match_dates[home_team] = match_date
                last_match_dates[away_team] = match_date

            match_date_index += 1
            if match_date_index >= len(match_dates):
                break



