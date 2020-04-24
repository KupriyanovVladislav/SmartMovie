import logging
from django.http import HttpResponse, Http404
from rest_framework import status
from django.views import View
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import Movie
from main.serializers import MovieSerializer, UserSerializer
from django.core.cache import cache


logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/index.html')


class MovieList(APIView):
    """
    List all movies, or create a new movie
    """

    def get(self, request):
        amount = 10
        movies = Movie.objects.prefetch_related('links')[:amount]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    """
    Retrieve, update or delete a Movie instance
    """
    # permission_classes = [permissions.AllowAny]

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


class MovieTopList(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        amount = self.validate_amount(self.request.query_params.get('amount', 10))
        result = {}
        if amount:
            result = cache.get(f'top_{amount}_films', {})
            if not result:
                movies = Movie.objects.filter(year__isnull=False).order_by('-year').prefetch_related('links')[:amount]
                serializer = MovieSerializer(movies, many=True)
                result = serializer.data
                cache.set(f'top_{amount}_films', result, 60*5)
        return Response(result)

    def validate_amount(self, amount):
        try:
            amount = int(amount)
            return amount
        except ValueError as exc:
            print(exc)
            return None
