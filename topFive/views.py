from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponse
from django.middleware.csrf import get_token

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.generics import get_object_or_404

from rest_framework_simplejwt.views import TokenObtainPairView
from .models import League, Team, CustomUser, Match
from .user_serializer import MyTokenObtainSerializer, RegisterSerializer, MatchSerializer
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Player
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .player_serializer import PlayerSerializer
import random


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                # Get the fifth league
                league = League.objects.get(level=5)
                print(f"League: {league.name}, Teams count: {league.teams.count()}")
                # Get all available teams in the fifth league
                available_teams = league.teams.filter(user=None)
                print(f"Available teams in League 5: {available_teams.count()}")
                if not available_teams.exists():
                    raise APIException("No available teams in League 5")

                # Choose a random available team
                team = random.choice(available_teams)
                team.user = user
                team.name = serializer.validated_data['team_name']
                team.arena = serializer.validated_data['arena_name']
                team.manager = serializer.validated_data['first_name'] + ' ' + serializer.validated_data['last_name']
                team.save()

                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            raise APIException(f"Error during registration: {str(e)}")


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful")
        else:
            return HttpResponse("Invalid credentials", status=400)
    return HttpResponse("Invalid request method", status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_league_teams(request):
    user = request.user

    try:
        # Get the user's team
        user_team = Team.objects.get(user=user)
        league = user_team.league
        teams = league.get_standings()
        sorted_teams = sorted(teams, key=lambda x: (-x.points, x.name))
        league_teams_data = [
            {
                'position': index + 1,
                'name': team.name,
                'manager_name': team.manager,
                'points': team.points
            }
            for index, team in enumerate(sorted_teams)
        ]
        return Response(league_teams_data, status=200)


    except Team.DoesNotExist:
        return Response({'error': 'Team not found for user.'}, status=404)
    except League.DoesNotExist:
        return Response({'error': 'League not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transfer_players(request):
    players = Player.objects.filter(transfer_list=True)
    serializer = PlayerSerializer(players, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_balance(request):
    user = request.user

    try:
        # Get the user's team
        user_team = Team.objects.get(user=user)
        # Return the current balance
        return Response({'balance': user_team.budget}, status=200)

    except Team.DoesNotExist:
        return Response({'error': 'Team not found for user.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_player(request):
    user = request.user
    player_id = request.data.get('player_id')
    try:
        player = Player.objects.get(id=player_id, transfer_list=True)
        user_team = Team.objects.get(user=user)

        # Check if user has enough budget
        if user_team.budget < player.price:
            return Response({'error': 'Insufficient budget'}, status=400)

        # Check if there is room in the team
        if user_team.players.count() >= 13:
            return Response({'error': 'No space in the team'}, status=400)

        # Perform the purchase
        user_team.budget -= player.price
        user_team.add_player(player)
        player.free_agent = False
        player.team = user_team
        player.save()
        user_team.save()

        return Response({
            'message': 'Player bought successfully',
            'new_balance': user_team.budget
        }, status=200)

    except Player.DoesNotExist:
        return Response({'error': 'Player not found'}, status=404)
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_coach(request):
    team = Team.objects.get(user=request.user)
    coach = team.coach
    return Response({
        'name': coach.name,
        'defense': coach.defense,
        'offense': coach.offense,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_players(request):
    team = Team.objects.get(user=request.user)
    players = team.players.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_team_info(request):
    try:
        team = Team.objects.get(user=request.user)
        players = team.players.all()  # קבלת כל השחקנים של הקבוצה
        player_serializer = PlayerSerializer(players, many=True)  # סריאליזציה של השחקנים
        return Response({
            'team_name': team.name,
            'manager': team.manager,
            'arena': team.arena,
            'points': team.points,
            'position': team.position,
            'budget': team.budget,  # הוספת תקציב לתגובה
            'players': player_serializer.data,  # הוספת שחקנים לתגובה
        }, status=200)
    except Team.DoesNotExist:
        return Response({'error': 'Team not found for user.'}, status=404)


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        team = get_object_or_404(Team, user=user)
        return Match.objects.filter(league=team.league)
