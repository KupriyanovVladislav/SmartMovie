import requests
import os


class TmdbAPI:
    BASE_URL = 'https://api.themoviedb.org/3/movie/{movie_id}'
    BASE_IMAGE_URL = 'https://image.tmdb.org/t/p/{size}{path}'
    AUTH_TOKEN = os.getenv('TMDB_TOKEN')

    def get_movie_details(self, movie_id, more=False):
        movie_details = {}
        if not self.AUTH_TOKEN:
            return movie_details

        if not isinstance(movie_id, int):
            try:
                movie_id = int(movie_id)
            except TypeError:
                return movie_details

        url = self.BASE_URL.format(movie_id=movie_id)
        data = self.fetch(url, params={'api_key': self.AUTH_TOKEN})
        if not data:
            movie_details = data
        else:
            movie_details = self._composite_movie_data(data, more)

        return movie_details

    @staticmethod
    def fetch(url: str, params: dict):
        data = {}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
        return data

    def _composite_movie_data(self, data: dict, more: bool):
        result = {}
        if more:
            fields = (
                'poster_path', 'overview', 'release_date', 'budget',
                'runtime', 'production_countries', 'vote_average',
            )
            for field in fields:
                result[field] = data.get(field, None)
            if result['poster_path']:
                result['poster_path'] = self.BASE_IMAGE_URL.format(size='w300', path=result['poster_path'])
        else:
            backdrop = data.get('backdrop_path', None)
            result['backdrop_path'] = self.BASE_IMAGE_URL.format(size='w500', path=backdrop) if backdrop else backdrop

        return result
