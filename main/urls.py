from django.urls import path
from main import views

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('auth/register/', views.CreateUserView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogOutView.as_view())
]