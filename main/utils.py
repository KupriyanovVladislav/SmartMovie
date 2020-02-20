import pandas as pd
import re
from .models import Movie, Link, Rating, Tag


class MoviesFilePreprocessor:
    PATH = 'data/movies.csv'
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
