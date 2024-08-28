# topFive/tasks.py

from celery import shared_task
from topFive.models import Match
from topFive.management.commands.simulate_match import simulate_all_matches


@shared_task
def simulate_matches_task():
    simulate_all_matches()
