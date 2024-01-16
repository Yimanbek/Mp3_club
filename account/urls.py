from django.urls import path
from .views import RegistrationView,LoginView,DashboardView,activation_view,ResetPasswordView,ResetView,ActivationView

urlpatterns = [
    path('register/',RegistrationView.as_view(),name='registration'),
    path('login/',LoginView.as_view(),name='login'),
    path('dashboard/',DashboardView.as_view(),name = 'dashboard'),
    path('activation/',activation_view , name='activation'),
    path('activate/',ActivationView.as_view()),
    path('reset_passwrod_1/',ResetView.as_view(),name='reset_password_1'),
    path('reset_password_2/', ResetPasswordView.as_view(), name='reset_password_2'),
]