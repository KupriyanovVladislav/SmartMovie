from django.http import HttpResponse, Http404
from rest_framework import status
from django.views import View
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Movie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import MovieSerializer, UserSerializer


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')


class MovieList(APIView):
    """
    List all movies, or create a new movie
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        movies = Movie.objects.all()[:10]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    """
    Retrieve, update or delete a Movie instance
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

