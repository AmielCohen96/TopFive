from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from topFive.models import CustomUser, Match, League, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.profile.email
        token['bio'] = user.profile.bio
        token['verified'] = user.profile.verified

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    team_name = serializers.CharField(max_length=100, required=True)
    arena_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'team_name', 'arena_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Check if the email is already in use
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise ValidationError("This email address is already in use.")

        # Check if the username is already in use
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise ValidationError("This username is already in use.")

        # Check if the team name is already in use
        if CustomUser.objects.filter(team_name=attrs['team_name']).exists():
            raise ValidationError("This team name is already in use.")

        return attrs

    def create(self, validated_data):
        # Remove the password2 field

        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            team_name=validated_data['team_name'],
            arena_name=validated_data['arena_name'],
        )
        return user


# Create a serializer for the League model
# Create a serializer for the League model
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'level']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'league']


class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()  # Use nested serializer to include home team details
    away_team = TeamSerializer()  # Use nested serializer to include away team details
    league = LeagueSerializer()

    class Meta:
        model = Match
        fields = ['id', 'league', 'home_team', 'away_team', 'home_team_score', 'away_team_score', 'match_date',
                  'completed']
