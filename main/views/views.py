import logging
from django.http import Http404
from rest_framework import status, filters, permissions, generics
from django.views import View
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import Movie, Bookmark
from main.serializers import MovieSerializer, MovieMoreInfoSerializer, BookmarkSerializer, RatingSerializer
from django.core.cache import cache
from time import time
from ..recommendations import searcher


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
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = MovieMoreInfoSerializer(movie, user=request.user)
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
        # cache.delete('top_5_films')
        if amount:
            result = cache.get(f'top_{amount}_films', {})
            if not result:
                movies = Movie.objects.filter(year__isnull=False).order_by('-year').prefetch_related('links')[:amount]
                serializer = MovieSerializer(movies, many=True)
                result = serializer.data
                cache.set(f'top_{amount}_films', result, 60*1)
        return Response(result)

    def validate_amount(self, amount):
        try:
            amount = int(amount)
            return amount
        except ValueError as exc:
            print(exc)
            return None


class MovieSearchByNameListView(generics.ListAPIView):
    """
    List all movies starts with search
    """
    permission_classes = [permissions.AllowAny]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


class BookmarkList(APIView):
    def get(self, request):
        bookmarks = Bookmark.objects.filter(user_id=request.user.id)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        data['timestamp'] = int(time())
        serializer = BookmarkSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarkDetail(APIView):
    def get_object(self, pk):
        try:
            return Bookmark.objects.get(id=pk)
        except Bookmark.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        bookmark = self.get_object(pk)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SimilarMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        similar_movies = self.find_similar_movies()
        similar_movies = Movie.objects.filter(title__in=similar_movies).prefetch_related('links')
        serializer = MovieSerializer(similar_movies.reverse(), many=True)
        return Response(serializer.data)

    def find_similar_movies(self):
        title = self.request.query_params.get('title', None)
        amount = self.validate_amount(self.request.query_params.get('top', 5))
        similar_movies = searcher.get(title, int(amount))
        return similar_movies

    def validate_amount(self, amount):
        result = 10
        try:
            result = int(amount)
        finally:
            return result


class RatingList(APIView):
    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id
        data['is_archived'] = False
        data['timestamp'] = int(time())
        serializer = RatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
