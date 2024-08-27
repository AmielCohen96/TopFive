from django.core.management import BaseCommand

from topFive.models import Match


class Command(BaseCommand):
    help = 'Simulate matches for all leagues'

    def handle(self, *args, **kwargs):
        self.stdout.write('Simulating matches...')
        simulate_matches()
        self.stdout.write(self.style.SUCCESS('Successfully simulated all matches'))


def simulate_matches():
    matches = Match.objects.filter(played=False)
    for match in matches:
        match.play_match()
