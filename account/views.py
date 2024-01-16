from django.shortcuts import render,redirect
from django.views import View
from .serializers import RegistrationSerializer,ActivationSerializer,ResetPasswordSerializer
from rest_framework import status
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView , get_object_or_404,ListAPIView
from django.contrib.auth import get_user_model,authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .send_email import send_confirmation_email,send_confirmation_password
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib import messages

User = get_user_model()

class RegistrationView(APIView):
    templates_name = 'registration.html'

    def get(self, request):
        return render(request, self.templates_name)

    def post(self, request):
        if request.data.get('is_author', False) == 'on':
            is_author = True
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_author=is_author)
            if user:
                try:
                    send_confirmation_email(user.email, user.activation_code)
                    return redirect('dashboard')
                except:
                    return Response({'message': "Зарегистрировался, но на почту код не отправился", 'data': serializer.data}, status=201)
            return Response({'message': 'User registered successfully'}, status=201)
        else:
            return render(request, self.templates_name, {'error': serializer.errors})

def activation_view(request):
    return render(request, 'activation.html')

class DashboardView(View):
    templates_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.templates_name)
    
    def post(self, request):
        action = request.POST.get('action', None)

        if action == 'login':
            return redirect('login')
        elif action == 'register':
            return redirect('registration')
        else:
            error_message = 'Invalid action'
            return render(request, self.templates_name, {'error': error_message})

        

class LoginView(View):
    templates_name = 'login.html'
    
    def get(self, request):
        return render(request, self.templates_name)
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            return render(request, self.templates_name, {'error': 'Email and Password are required!'})
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            
            if created:
                return HttpResponseRedirect(reverse('dashboard') + f'?token={token.key}')
            else:
                return HttpResponseRedirect(reverse('dashboard') + f'?token={token.key}')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, self.templates_name)


class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer

    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.save()
        return redirect('activation')
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return redirect('activation')
    

class ResetView(APIView):
    templates_name = 'reset_password_1.html'


    def get(self, request):
        return render(request, self.templates_name)
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return render(request,self.templates_name,{'error': 'Пожалуйста, укажите электронный адрес'})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request,self.templates_name,{'error': 'Пользователь с указанным адресом не найден'})
        password_change_code = user.create_number_code()
        user.password_change_code = password_change_code
        user.save()
        send_confirmation_password(user.email,password_change_code)

        return redirect('reset_password_2')
    

class ResetPasswordView(View):
    template_name = 'reset_password_2.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        if not email:
            return render(request, self.template_name, {'error': 'Пожалуйста, укажите электронный адрес'})
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'Пользователь с указанным адресом не найден'})
        
        serializer = ResetPasswordSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')

        return render(request, self.template_name, {'error': serializer.errors})

