# classes/player.py
import random
from faker import Faker
fake = Faker()


class Player:
    def __init__(self, name, age, height, position, speed, strength, stamina, shooting3, shooting2, jumping, defense):
        self.name = name
        self.age = age
        self.height = height
        self.position = position
        self.speed = speed
        self.strength = strength
        self.stamina = stamina
        self.shooting3 = shooting3
        self.shooting2 = shooting2
        self.jumping = jumping
        self.defense = defense
        self.team = None
        self.rating = int((self.speed + self.strength + self.stamina + self.shooting3 + self.shooting2 +
                           self.jumping + self.defense) / 7)

    def __init__(self, name=None, age=None, height=None, position=None, speed=None, strength=None, stamina=None,
                 shooting3=None, shooting2=None, jumping=None, defense=None):
        self.name = fake.first_name_male() + ' ' + fake.last_name_male()
        self.age = age if age else random.randint(17, 39)
        self.height = height if height else round(random.uniform(1.78, 2.22), 2)
        self.position = position if position else random.randint(1, 5)
        self.speed = speed if speed else random.randint(60, 100)
        self.strength = strength if strength else random.randint(60, 100)
        self.stamina = stamina if stamina else random.randint(60, 100)
        self.shooting3 = shooting3 if shooting3 else random.randint(60, 100)
        self.shooting2 = shooting2 if shooting2 else random.randint(60, 100)
        self.jumping = jumping if jumping else random.randint(60, 100)
        self.defense = defense if defense else random.randint(60, 100)
        self.team = None
        self.rating = int((self.speed + self.strength + self.stamina + self.shooting3 + self.shooting2 +
                           self.jumping + self.defense) / 7)

    def update_stats(self, speed=None, strength=None, stamina=None, shooting3=None, shooting2=None, jumping=None, defense=None):
        if speed:
            self.speed = speed
        if strength:
            self.strength = strength
        if stamina:
            self.stamina = stamina
        if shooting3:
            self.shooting3 = shooting3
        if shooting2:
            self.shooting2 = shooting2
        if jumping:
            self.jumping = jumping
        if defense:
            self.defense = defense
        self.rating = int((self.speed + self.strength + self.stamina + self.shooting3 + self.shooting2 +
                           self.jumping + self.defense) / 7)

