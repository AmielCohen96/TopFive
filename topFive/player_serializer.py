# topFive/serializers.py
from rest_framework import serializers
from .models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = '__all__'

    def get_team(self, obj):
        return obj.team.name if obj.team else None
