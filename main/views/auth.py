from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
    API for creating User
    """
    model = User
    serializer_class = UserSerializer


class LoginView(APIView):
    """
    API for login not authorized USER
    """
    def post(self, request):
        success, message = False, ''
        if request.user.is_anonymous:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                success, message = True, 'You successfully login'
                login(request, user)
        else:
            message = 'You have already been authorized'

        return Response({'success': success, 'message': message})


class LogOutView(APIView):
    """
    API for logout authorized USER
    """
    def get(self, request):
        success, message = False, ''
        if request.user.is_authenticated:
            logout(request)
            success, message = True, "You successfully logout"
        else:
            message = "You haven't been authorized"

        return Response({'success': success, 'message': message})


class ResetPasswordView(APIView):
    pass
