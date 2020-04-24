import requests
import os


class TmdbAPI:
    BASE_URL = 'https://api.themoviedb.org/3/movie/{movie_id}'
    BASE_IMAGE_URL = 'https://image.tmdb.org/t/p/{size}/{path}'
    AUTH_TOKEN = os.getenv('TMDB_TOKEN')

    def get_movie_details(self, movie_id):
        movie_details = {}
        if not self.AUTH_TOKEN:
            return movie_details

        if not isinstance(movie_id, int):
            try:
                movie_id = int(movie_id)
            except TypeError:
                return movie_details

        url = self.BASE_URL.format(movie_id=movie_id)
        print(url)
        response = requests.get(url, params={'api_key': self.AUTH_TOKEN})
        if response.status_code == 200:
            data = response.json()
            image_path = data['backdrop_path']
            image_path = image_path[1:] if image_path else image_path
            if image_path:
                movie_details['image_url'] = self.BASE_IMAGE_URL.format(size='w500', path=image_path)
            else:
                movie_details['image_url'] = image_path

        return movie_details
