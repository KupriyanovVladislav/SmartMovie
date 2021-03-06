from django.urls import path
from main.views import views
from main.views import auth
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('movies/top/', views.MovieTopList.as_view()),
    path('movies/searchByName/', views.MovieSearchByNameListView.as_view()),
    path('movies/similar/', views.SimilarMoviesView.as_view()),
    path('token-auth/', obtain_jwt_token),
    path('current_user/', auth.current_user),
    path('users/', auth.UserList.as_view()),
    path('bookmarks/', views.BookmarkList.as_view()),
    path('bookmarks/<int:pk>', views.BookmarkDetail.as_view()),
    path('ratings/', views.RatingList.as_view()),
    path('users/recommendations/', views.SimilarMoviesForUserView.as_view()),
]
