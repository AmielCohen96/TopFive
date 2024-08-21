# classes/league.py
import random
from faker import Faker
fake = Faker()


class League:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.teams = []

    def __init__(self, name=None, level=None):
        self.name = name if name else f"League-{random.randint(1, 100)}"
        self.level = level if level else random.randint(1, 5)
        self.teams = []

    def add_team(self, team):
        if len(self.teams) < 10:
            self.teams.append(team)
        else:
            raise ValueError("A league can only have 10 teams")

    def get_teams(self):
        return self.teams

    def get_standings(self):
        return sorted(self.teams, key=lambda x: x.points, reverse=True)
