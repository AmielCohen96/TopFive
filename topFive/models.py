from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    arena_name = models.CharField(max_length=100, blank=True, null=True)
    USERNAME_FIELD = 'username'

    def edit_points(self, new_points):
        self.points = new_points
        self.save()

    class Meta:
        app_label = 'topFive'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def edit_position(self, new_position):
        self.position = new_position
        self.save()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=CustomUser)
post_save.connect(save_user_profile, sender=CustomUser)


# Functions to generate default values
def get_default_defense():
    return random.randint(60, 100)


def get_default_offense():
    return random.randint(60, 100)


def get_default_age():
    return random.randint(17, 39)


def get_default_height():
    return round(random.uniform(1.78, 2.22), 2)


def get_default_position():
    return random.randint(1, 5)


def get_default_stat():
    return random.randint(60, 100)


def get_default_level():
    return random.randint(1, 5)


# Models
class Coach(models.Model):
    name = models.CharField(max_length=100)
    defense = models.IntegerField(default=get_default_defense)
    offense = models.IntegerField(default=get_default_offense)
    # No team field here to avoid confusion


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=get_default_age)
    height = models.FloatField(default=get_default_height)
    position = models.IntegerField(default=get_default_position)
    speed = models.IntegerField(default=get_default_stat)
    strength = models.IntegerField(default=get_default_stat)
    stamina = models.IntegerField(default=get_default_stat)
    shooting3 = models.IntegerField(default=get_default_stat)
    shooting2 = models.IntegerField(default=get_default_stat)
    jumping = models.IntegerField(default=get_default_stat)
    defense = models.IntegerField(default=get_default_stat)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(editable=False, default=0)  # Use editable=False if you don't want to edit this field

    @property
    def rating_(self):
        return int((self.speed + self.strength + self.stamina + self.shooting3 + self.shooting2 +
                    self.jumping + self.defense) / 7)

    def update_stats(self, speed=None, strength=None, stamina=None, shooting3=None, shooting2=None, jumping=None,
                     defense=None):
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
        self.save()


class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='teams')
    players = models.ManyToManyField(Player, related_name='teams', blank=True)
    budget = models.IntegerField(default=1000000)
    league = models.ForeignKey('League', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    position = models.IntegerField(null=True, blank=True)
    average_rating = models.IntegerField(default=0)
    arena = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def add_player(self, player):
        if self.players.count() < 13:
            self.players.add(player)
            player.team = self
            self.update_average_rating()
        else:
            raise ValueError("A team can only have 13 players")

    def remove_player(self, player):
        if player in self.players.all() and self.players.count() > 9:
            self.players.remove(player)
            player.team = None
            self.update_average_rating()

    def update_average_rating(self):
        if self.players.count() > 0:
            total_rating = sum(player.rating for player in self.players.all())
            self.average_rating = int(total_rating / self.players.count())
        else:
            self.average_rating = 0
        self.save()

    def edit_name(self, new_name):
        self.name = new_name
        self.save()

    def edit_coach(self, new_coach):
        self.coach = new_coach
        self.save()

    def edit_budget(self, new_budget):
        self.budget = new_budget
        self.save()

    def edit_arena(self, new_arena):
        self.arena = new_arena
        self.save()


class League(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()
    teams = models.ManyToManyField(Team, related_name='leagues', blank=True)

    def add_team(self, team):
        if self.teams.count() < 10:
            self.teams.add(team)
        else:
            raise ValueError("A league can only have 10 teams")

    def get_teams(self):
        return self.teams.all()

    def get_standings(self):
        return sorted(self.teams.all(), key=lambda x: x.points, reverse=True)

    # Override the related_name attributes for the reverse relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Ensure unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Ensure unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser'
    )
