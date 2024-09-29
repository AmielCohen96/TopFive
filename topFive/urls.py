# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
# from . import views as users_views, views
# from django.contrib.auth import views as auth_views
# from .views import get_csrf_token, MatchViewSet, trigger_simulation
#
# match_list = MatchViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# match_detail = MatchViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# urlpatterns = [
#     path("token/", views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
#     path("token/verify/", TokenVerifyView.as_view(), name='token_verify'),
#     path("csrf/", views.get_csrf_token, name='csrf_token'),
#     path('signup/', users_views.RegisterView.as_view(), name='signup'),
#     path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view, name='logout'),
#     path('league-teams/', views.get_league_teams, name='league_teams'),
#     path('transfer-players/', views.get_transfer_players, name='transfer_players'),
#     path('current-balance/', views.get_current_balance, name='current-balance'),
#     path('buy-player/', views.buy_player, name='buy-player'),
#     path('my-coach/', views.get_my_coach, name='my-coach'),
#     path('my-players/', views.get_my_players, name='my-players'),
#     path('user-team-info/', views.get_user_team_info, name='user_team_info'),
#     path('matches/', match_list, name='matches'),
#     path('matches/<int:pk>/', match_detail, name='match_detail'),
#     path('simulate/', trigger_simulation, name='trigger_simulation')
# ]


from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views as users_views
from django.contrib.auth import views as auth_views
from .views import get_csrf_token, MatchViewSet, trigger_simulation, real_time_match_update

match_list = MatchViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

match_detail = MatchViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path("token/", users_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name='token_verify'),
    path("csrf/", get_csrf_token, name='csrf_token'),
    path('signup/', users_views.RegisterView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('league-teams/', users_views.get_league_teams, name='league_teams'),
    path('transfer-players/', users_views.get_transfer_players, name='transfer_players'),
    path('current-balance/', users_views.get_current_balance, name='current_balance'),
    path('buy-player/', users_views.buy_player, name='buy_player'),
    path('my-coach/', users_views.get_my_coach, name='my_coach'),
    path('my-players/', users_views.get_my_players, name='my_players'),
    path('user-team-info/', users_views.get_user_team_info, name='user_team_info'),
    path('matches/', match_list, name='matches'),
    path('matches/<int:pk>/', match_detail, name='match_detail'),
    path('simulate/', trigger_simulation, name='trigger_simulation'),
    path('matches/<int:pk>/real-time/', real_time_match_update, name='real_time_match_update'),

]
