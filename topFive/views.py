from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to a home page or any other page
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
