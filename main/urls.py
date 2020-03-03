from django.urls import path
from main import views

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('register/', views.CreateUserView.as_view()),
    path('login/', views.LoginView.as_view()),
]