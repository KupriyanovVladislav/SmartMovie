from django.http import HttpResponse, Http404
from rest_framework import status
from django.views import View
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.models import Movie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.serializers import MovieSerializer, UserSerializer


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