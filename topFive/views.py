from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from topFive.user_serializer import UserSerializer


class IndexView(TemplateView):
    template_name = "index.html"

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'User created successfully!'}, status=201)
            # Include the errors in the response for debugging
            return JsonResponse({'errors': serializer.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid username or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)




# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False}, status=400)


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)