import pandas as pd
from numpy import mean, size
from ..models import Movie, Rating


class SimilarMoviesSearcher:
    """
    To get similar movies, use method get(movie_name, amount), where
    movie_name: str,  movie name, for which you want get similar movies.
    amount: int, amount of similar movies.
    """
    RATING_COLS = ('user_id', 'movie_id', 'rating')
    MOVIE_COLS = ('movie_id', 'title')
    RATING_COUNT = 100

    def __init__(self):
        self.ratings = self._init_ratings()
        self.user_movie_table = self._init_user_movie_table()
        self.popular_movies = self._init_popular_movies()

    def _init_ratings(self):
        """
        :return: DataFrame with columns: user_id, movie_id, rating, title
        """
        ratings = pd.DataFrame(list(Rating.objects.all().values(*self.RATING_COLS)))
        movies = pd.DataFrame(list(Movie.objects.all().values(*self.MOVIE_COLS)))
        ratings = pd.merge(ratings, movies)
        return ratings

    def _init_user_movie_table(self):
        """
        :return: matrix(DataFrame), where
            rows - users,
            columns - titles,
            values - ratings by user to movie.
        """
        user_movie_table = self.ratings.pivot_table(index='user_id', columns='title', values='rating')
        return user_movie_table

    def _init_popular_movies(self):
        """
        :return: DataFrame with popular movies. Popular movies are defined by their amount of ratings.
        Columns of returning DataFrames: title, rating size(amount of ratings), mean(mean rating)
        """
        movie_stats = self.ratings.groupby('title').agg({'rating': [size, mean]})
        popular_movies = movie_stats['rating']['size'] >= self.RATING_COUNT
        return movie_stats[popular_movies]

    def get(self, movie_name: str, amount=10) -> list:
        """
        :param movie_name: str,  movie name, for which you want get similar movies.
        :param amount: int, amount of similar movies
        :return: list, containing similar movies
        """
        result = []
        movie_rating = self.user_movie_table.get(movie_name, None)
        if not(movie_rating is None):
            similar_movies = self.user_movie_table.corrwith(movie_rating).dropna()
            df = self.popular_movies.join(pd.DataFrame(similar_movies, columns=['similarity']))
            result_df = df.sort_values(['similarity'], ascending=False)[:amount + 1]
            result = list(result_df.index[1:])
        return result
