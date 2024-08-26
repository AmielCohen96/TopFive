# topFive/serializers.py
from rest_framework import serializers
from .models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'age', 'height', 'position_name', 'rating', 'price', 'team']

    def get_team(self, obj):
        return obj.team.name if obj.team else None
