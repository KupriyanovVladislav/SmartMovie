import pandas as pd
import re
from .models import Movie, Link, Rating, Tag
import csv
from .serializers import UserSerializer


class MoviesFilePreprocessor:
    PATH = 'main/data/movies.csv'
    YEAR_REGEX = r'\((\d{4})\)'
    SPLIT_SYMBOL = '|'

    @staticmethod
    def csv_file_to_dict(path: str) -> dict:
        data = {}
        try:
            data = pd.read_csv(path).set_index('movieId').to_dict('index')
        except FileNotFoundError as e:
            pass
        return data

    def run(self) -> dict:
        data = self.csv_file_to_dict(self.PATH)
        for key in data.keys():
            year = self.extract_year(data[key])
            if year:
                data[key]['year'] = year
            else:
                data[key]['year'] = None
            data[key]['genres'] = self.extract_genres(data[key])
        return data

    def extract_year(self, item):
        match = re.findall(self.YEAR_REGEX, item['title'])
        result = match[0] if match else None
        return result

    def extract_genres(self, item):
        return item['genres'].split(self.SPLIT_SYMBOL)


def update_movie_table():
    data = MoviesFilePreprocessor().run()
    if Movie.objects.all():
        Movie.objects.all().delete()
    movie_objects = [
        Movie(movie_id=key, title=data[key]['title'], year=data[key]['year'], genres=data[key]['genres'])
        for key in data.keys()
    ]
    Movie.objects.bulk_create(movie_objects)


def update_link_table():
    if Link.objects.all():
        Link.objects.all().delete()
    with open('main/data/links.csv') as f:
        reader = csv.reader(f)
        next(reader)
        link_objects = [
            Link(
                movie_id=row[0],
                imdb_id=row[1] if row[1] else None,
                tmdb_id=row[2] if row[2] else None
            )
            for row in reader
        ]
        Link.objects.bulk_create(link_objects)


def update_rating_table():
    if Rating.objects.all():
        Rating.objects.all().delete()
    with open('main/data/ratings.csv') as f:
        reader = csv.reader(f)
        next(reader)
        rating_objects = [
            Rating(
                user_id=row[0],
                movie_id=row[1],
                rating=row[2],
                timestamp=row[3] if row[3] else None
            )
            for row in reader
        ]
        Rating.objects.bulk_create(rating_objects)


def update_tag_table():
    if Tag.objects.all():
        Tag.objects.all().delete()
    with open('main/data/tags.csv') as f:
        reader = csv.reader(f)
        next(reader)
        tag_objects = [
            Tag(
                user_id=row[0],
                movie_id=row[1],
                tag=row[2] if row[2] else None,
                timestamp=row[3] if row[3] else None
            )
            for row in reader
        ]
        Tag.objects.bulk_create(tag_objects)


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
