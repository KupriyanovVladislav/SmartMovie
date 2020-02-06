import pandas as pd
import re


class MoviesFileEditor:
    PATH = 'data/movies.csv'
    YEAR_REGEX = ''
    GENRES_REGEX = ''

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
        return data

    def extract_year(self, item):
        pass

    def extract_genres(self, item):
        pass


print(MoviesFileEditor().run())
