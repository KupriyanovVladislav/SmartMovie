from rest_framework import serializers
from .models import Movie, Link
from django.contrib.auth.models import User


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('imdb_id', 'tmdb_id')


class MovieSerializer(serializers.ModelSerializer):
    links = LinkSerializer(read_only=True)

    class Meta:
        model = Movie
        depth = 1
        fields = ('movie_id', 'title', 'year', 'genres', 'links')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password', )
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
