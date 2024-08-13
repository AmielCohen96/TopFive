from django.urls import path
from .views import IndexView, signup_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', signup_view, name='signup'),

]