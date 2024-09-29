import os
from datetime import datetime, timedelta

import django
from django.core.management.base import BaseCommand
from topFive.models import Coach, Player, Team, League, Match
from faker import Faker

from .league_create import create_match
from .simulate_match import simulate_all_matches

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Top5.settings')

django.setup()

fake = Faker()


class Command(BaseCommand):
    help = 'Creates initial data for the project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating leagues and teams...')
        create_leagues_and_teams()
        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))


def create_leagues_and_teams():
    league_names = ["First League", "Second League", "Third League", "Fourth League", "Fifth League"]
    leagues = []

    for idx, name in enumerate(league_names):
        league = League.objects.create(name=name, level=idx + 1)
        leagues.append(league)

    free_agents = []  # List of free agents

    for league in leagues:
        teams = []
        for _ in range(10):  # Create 10 teams in each league
            coach = Coach.objects.create(name=fake.first_name() + ' ' + fake.last_name())
            players = [Player.objects.create(name=fake.first_name() + ' ' + fake.last_name()) for _ in range(10)]
            team = Team.objects.create(
                name=fake.city(),
                manager=fake.first_name() + ' ' + fake.last_name(),
                coach=coach,
                budget=1000000,
                league=league,
                arena=fake.company()
            )
            team.players.set(players)
            for player in players:
                player.team = team
                player.save()  # Players with teams are not free agents
            team.update_average_rating()
            team.save()

            # Add the team to the league
            league.teams.add(team)
            teams.append(team)

    # Create 100 additional free agent players
    for _ in range(100):
        player = Player.objects.create(name=fake.first_name() + ' ' + fake.last_name())
        free_agents.append(player)

    # Update all free agent players
    for player in free_agents:
        player.save()  # Calculate rating and price for each free agent

    # Update average rating of all teams
    teams = Team.objects.all()
    for team in teams:
        team.update_average_rating()


create_match()
simulate_all_matches()


