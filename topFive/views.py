from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import League, Team, CustomUser
from .user_serializer import MyTokenObtainSerializer, RegisterSerializer
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
    if not user.team_name:
        return Response({'error': 'User does not have a team assigned.'}, status=400)

    try:
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
