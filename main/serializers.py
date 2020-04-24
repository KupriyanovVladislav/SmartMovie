from rest_framework import serializers
from .models import Movie, Link
from .models import User
from rest_framework_jwt.settings import api_settings
from .utils.tmdbApi import TmdbAPI


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('imdb_id', 'tmdb_id')


class MovieSerializer(serializers.ModelSerializer):
    links = LinkSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        depth = 1
        fields = ('movie_id', 'title', 'year', 'genres', 'links', 'image')

    def get_image(self, obj):
        movie_details = TmdbAPI().get_movie_details(obj.links.tmdb_id)
        image = None
        if 'image_url' in movie_details:
            image = movie_details['image_url']
        return image


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
