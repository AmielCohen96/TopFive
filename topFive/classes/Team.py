# classes/team.py
import random
from .Coach import Coach
from .Player import Player
from faker import Faker
fake = Faker()


class Team:
    def __init__(self, name, manager, coach,players, budget, league, arena):
        self.name = name
        self.manager = manager
        self.coach = coach
        self.players = players if len(players) >= 9 else []
        self.budget = budget
        self.league = league
        self.points = 0
        self.position = None
        self.average_rating = 0
        self.arena = arena

    def __init__(self, name=None, manager=None, coach=None, players=None, budget=None, league=None, arena=None):
        self.name = fake.city()
        self.manager = fake.first_name() + ' ' + fake.last_name()
        self.coach = coach if coach else Coach()
        self.players = players if players else [Player() for _ in range(random.randint(9, 13))]
        self.budget = 1000000
        self.league = league
        self.points = 0
        self.position = None
        self.average_rating = 0
        self.arena = arena if arena else fake.company()

    def add_player(self, player):
        if len(self.players) < 13:
            self.players.append(player)
            player.team = self
            self.update_average_rating()
        else:
            raise ValueError("A team can only have 13 players")

    def remove_player(self, player):
        if player in self.players and len(self.players) > 8:
            self.players.remove(player)
            player.team = None
            self.update_average_rating()

    def update_average_rating(self):
        if self.players:
            total_rating = sum(player.rating for player in self.players)
            self.average_rating = int(total_rating / len(self.players))
        else:
            self.average_rating = 0

    def edit_name(self, new_name):
        self.name = new_name
        self.save_to_db()

    def edit_coach(self, new_coach):
        self.coach = new_coach
        self.save_to_db()

    def edit_budget(self, new_budget):
        self.budget = new_budget
        self.save_to_db()

    def edit_arena(self, new_arena):
        self.arena = new_arena
        self.save_to_db()

    def edit_points(self, new_points):
        self.points = new_points
        self.save_to_db()

    def edit_position(self, new_position):
        self.position = new_position
        self.save_to_db()

    def save_to_db(self):
        pass


