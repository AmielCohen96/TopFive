# classes/coach.py
import random
from faker import Faker
fake = Faker()


class Coach:
    def __init__(self, name, defense, offense):
        self.name = name
        self.defense = defense
        self.offense = offense
        self.team = None

    def __init__(self, name=None, defense=None, offense=None):
        self.name = fake.first_name_male() + ' ' + fake.last_name_male()
        self.defense = defense if defense else random.randint(60, 100)
        self.offense = offense if offense else random.randint(60, 100)
        self.team = None

