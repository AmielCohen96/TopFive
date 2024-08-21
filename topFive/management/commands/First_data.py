import os
import django
from django.core.management.base import BaseCommand
from topFive.models import Coach, Player, Team, League
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


def create_leagues_and_teams():
    league_names = ["First League", "Second League", "Third League", "Fourth League", "Fifth League"]
    leagues = []

    for idx, name in enumerate(league_names):
        league = League.objects.create(name=name, level=idx + 1)
        leagues.append(league)

    for league in leagues:
        for _ in range(10):
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
                player.save()
            team.update_average_rating()
            team.save()

    # יצירת 100 שחקנים נוספים שאינם משויכים לקבוצה
    for _ in range(100):
        Player.objects.create(name=fake.first_name() + ' ' + fake.last_name())

    # עדכון כל השחקנים ללא שם ושיוך לקבוצה
    players = Player.objects.all()
    for player in players:
        if not player.name:
            player.name = fake.first_name() + ' ' + fake.last_name()
        if not player.team:
            team = Team.objects.order_by('?').first()  # בוחר קבוצה רנדומלית
            player.team = team
        player.save()

    # עדכון דירוג ממוצע של כל הקבוצות
    teams = Team.objects.all()
    for team in teams:
        team.update_average_rating()
