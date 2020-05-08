from rest_framework import serializers
from .models import Movie, Link, Bookmark
from .models import User
from rest_framework_jwt.settings import api_settings
from .utils.tmdbApi import TmdbAPI


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('imdb_id', 'tmdb_id')


class MovieSerializer(serializers.ModelSerializer):
    links = LinkSerializer(read_only=True)
    backdrop_path = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        depth = 1
        fields = ('movie_id', 'title', 'year', 'genres', 'links', 'backdrop_path')

    def get_backdrop_path(self, obj):
        movie_details = TmdbAPI().get_movie_details(obj.links.tmdb_id)
        image = None
        if 'backdrop_path' in movie_details:
            image = movie_details['backdrop_path']
        return image


class MovieMoreInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'movie_id', 'title', 'year', 'genres', 'links',
            'poster_path', 'overview', 'release_date', 'budget',
            'runtime', 'production_countries', 'vote_average'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmdb_api_handler = TmdbAPI()

    def to_representation(self, instance: Movie):
        result = {}
        tmdb_data = self.tmdb_api_handler.get_movie_details(instance.links.tmdb_id, more=True)
        for field in self.Meta.fields:
            if hasattr(instance, field):
                result[field] = getattr(instance, field)
            else:
                result[field] = tmdb_data.get(field, None)
        result['links'] = LinkSerializer(result['links']).data
        return result


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('token', 'email', 'password')

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data['password']
        instance = self.Meta.model(**validated_data)
        instance.clean_fields()
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class BookmarkSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bookmark
        fields = ('id', 'user_id', 'movie_id', 'timestamp', 'movie')

    def save(self, **kwargs):
        movie_id, user_id = self.validated_data['movie_id'], self.validated_data['user_id']
        if Bookmark.objects.filter(movie_id=movie_id, user_id=user_id).exists():
            self.instance = Bookmark.objects.get(movie_id=movie_id, user_id=user_id)
        super().save(**kwargs)

    def create(self, validated_data):
        bookmark = Bookmark(
            movie_id=validated_data['movie_id'],
            user_id=validated_data['user_id'],
            timestamp=validated_data['timestamp'],
        )
        bookmark.save()
        return bookmark
