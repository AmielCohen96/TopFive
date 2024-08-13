from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class IndexView(TemplateView):
    template_name = "index.html"


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')

            if password1 != password2:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            return JsonResponse({'message': 'User created successfully!'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
