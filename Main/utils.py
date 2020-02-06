import pandas as pd
import re


class MoviesFileEditor:
    PATH = 'data/movies.csv'
    YEAR_REGEX = r'\((\d{4})\)'
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
        for key in data.keys():
            year = self.extract_year(data[key])
            if year:
                data[key]['year'] = year
        return data

    def extract_year(self, item):
        match = re.findall(self.YEAR_REGEX, item['title'])
        result = match[0] if match else None
        return result

    def extract_genres(self, item):
        pass


print(MoviesFileEditor().run())
