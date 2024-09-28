from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from .serializers import UserSerializer
from .forms import UserForm
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        required_fields = ['username', 'password', 'email','age']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)
        form = UserForm(data)
        if form.is_valid():
            user = User.objects.create(
                username=data['username'],
                password=make_password(data['password']),  
                email=data['email'],
                age=data['age']
            )
            serializer = UserSerializer(user)
            return JsonResponse({'message':'Usuario creado correctamente','user':serializer.data}, status=201) 
        return JsonResponse({'error': form.errors}, status=400)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=403)  

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        required_fields = ['username', 'password']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        if not user.check_password(data['password']):
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=400)
        if user is None:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=400)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return JsonResponse({'token': access_token,'refresh': refresh_token}, status=200)