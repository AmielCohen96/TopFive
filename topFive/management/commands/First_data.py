import os
from datetime import datetime, timedelta

import django
from django.core.management.base import BaseCommand
from topFive.models import Coach, Player, Team, League, Match
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Top5.settings')


django.setup()

fake = Faker()


class Command(BaseCommand):
    help = 'Creates initial data for the project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating leagues and teams...')
        create_leagues_and_teams()
        self.stdout.write(self.style.SUCCESS('Successfully created initial data'))

#
# def create_leagues_and_teams():
#     league_names = ["First League", "Second League", "Third League", "Fourth League", "Fifth League"]
#     leagues = []
#
#     for idx, name in enumerate(league_names):
#         league = League.objects.create(name=name, level=idx + 1)
#         leagues.append(league)
#
#     free_agents = []  # רשימת שחקנים חופשיים
#
#     for league in leagues:
#         for _ in range(10):  # יצירת 10 קבוצות בכל ליגה
#             coach = Coach.objects.create(name=fake.first_name() + ' ' + fake.last_name())
#             players = [Player.objects.create(name=fake.first_name() + ' ' + fake.last_name()) for _ in range(10)]
#             team = Team.objects.create(
#                 name=fake.city(),
#                 manager=fake.first_name() + ' ' + fake.last_name(),
#                 coach=coach,
#                 budget=1000000,
#                 league=league,
#                 arena=fake.company()
#             )
#             team.players.set(players)
#             for player in players:
#                 player.team = team
#                 player.save()  # שחקנים עם קבוצות לא חופשיים (free agents)
#             team.update_average_rating()
#             team.save()
#
#             # הוסף את הקבוצה לליגה
#             league.teams.add(team)  # שורה זו מוסיפה את הקבוצה לליגה דרך שדה ה-ManyToMany של הליגה
#
#     # יצירת 100 שחקנים נוספים שאינם משויכים לקבוצה (שחקנים חופשיים)
#     for _ in range(100):
#         player = Player.objects.create(name=fake.first_name() + ' ' + fake.last_name())
#         free_agents.append(player)
#
#     # עדכון כל השחקנים החופשיים
#     for player in free_agents:
#         player.save()  # חישוב ה-rating והמחיר לכל שחקן חופשי
#
#     # עדכון דירוג ממוצע של כל הקבוצות
#     teams = Team.objects.all()
#     for team in teams:
#         team.update_average_rating()
#

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

        match_date = datetime.now() + timedelta(days=7)
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                Match.objects.create(home_team=teams[i], away_team=teams[j], match_date=match_date)
                Match.objects.create(home_team=teams[j], away_team=teams[i], match_date=match_date)

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

