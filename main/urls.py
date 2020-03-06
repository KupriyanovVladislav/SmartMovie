from django.urls import path
from main.views import views
from main.views import auth

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('auth/register/', auth.CreateUserView.as_view()),
    path('auth/login/', auth.LoginView.as_view()),
    path('auth/logout/', auth.LogOutView.as_view())
]