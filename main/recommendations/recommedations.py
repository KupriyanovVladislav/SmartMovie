import pandas as pd
import numpy as np
from main.models import Movie, Rating
from functools import cmp_to_key


class SimilarMoviesSearcher:
    """
    To get similar movies, use method get(movie_name, amount), where
    movie_name: str,  movie name, for which you want get similar movies.
    amount: int, amount of similar movies.
    """
    RATING_COLS = ('user_id', 'movie_id', 'rating')
    MOVIE_COLS = ('movie_id', 'title')
    RATING_COUNT = 50

    def __init__(self):
        self.ratings = self._init_ratings()
        self.search_table = self._init_search_table()
        self.popular_movies = self._init_popular_movies()
        self.popular_movie_user_table = self._init_popular_movie_user_table()

    def _init_ratings(self):
        """
        :return: DataFrame with columns: userId, movieId, rating, title
        """
        ratings = pd.DataFrame(list(Rating.objects.all().values(*self.RATING_COLS)))
        movies = pd.DataFrame(list(Movie.objects.all().values(*self.MOVIE_COLS)))
        ratings = pd.merge(ratings, movies)
        return ratings

    def _init_search_table(self):
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
        movie_stats = self.ratings.groupby('title').agg({'rating': [np.size, np.mean]})
        popular_movies = movie_stats['rating']['size'] >= self.RATING_COUNT
        return movie_stats[popular_movies]

    def _init_popular_movie_user_table(self):
        """
        :return: matrix(DataFrame), where
            rows - users,
            columns - titles of popular films having >= self.RATING_COUNT,
            values - ratings by user to movie.
        """
        ratings_ = self.ratings.set_index('title')
        popular_ratings = self.popular_movies.join(ratings_)
        popular_movie_ratings = popular_ratings.pivot_table(index=['user_id'], columns=['title'], values='rating')
        return popular_movie_ratings

    @staticmethod
    def _sort_movies(movie_name, movie_similarity: dict) -> list:
        first_word = movie_name.split()[0]

        def comparator(movie_1, movie_2):
            if movie_1[0].startswith(first_word) and movie_2[0].startswith(first_word):
                compare_values(movie_1[1], movie_2[1])
            elif movie_1[0].startswith(first_word):
                return 1
            elif movie_2[0].startswith(first_word):
                return -1
            else:
                compare_values(movie_1[1], movie_2[1])

        def compare_values(val_1, val_2):
            if val_1 > val_2:
                return 1
            else:
                return -1

        sorted_movies = sorted(list(movie_similarity.items()), key=cmp_to_key(comparator), reverse=True)
        return [movie[0] for movie in sorted_movies]

    def get(self, movie_name: str, amount: int) -> list:
        """
        :param movie_name: str,  movie name, for which you want get similar movies.
        :param amount: int, amount of similar movies
        :return: list, containing similar movies
        """
        result = []
        movie_rating = self.search_table.get(movie_name, None)
        if not(movie_rating is None):
            similar_movies = self.popular_movie_user_table.corrwith(movie_rating).dropna()
            df = self.popular_movies.join(pd.DataFrame(similar_movies, columns=['similarity']))
            result_df = df.sort_values(['similarity'], ascending=False)['similarity'][:amount*5]
            if movie_name in result_df:
                result_df = result_df.drop(movie_name)
            result = self._sort_movies(movie_name, result_df)
        return result[:amount]
