from django.contrib.auth.views import LoginView
from django.urls import path
from .views import IndexView, signup_view, login_view, logout_view

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]