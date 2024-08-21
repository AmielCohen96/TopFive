from django.contrib import admin
from .models import Coach, Player, Team, League

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'defense', 'offense')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'age', 'height', 'position', 'speed', 'strength', 'stamina',
        'shooting3', 'shooting2', 'jumping', 'defense', 'rating'
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'coach', 'budget', 'league', 'points', 'position', 'average_rating', 'arena')
    filter_horizontal = ('players',)

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    filter_horizontal = ('teams',)
