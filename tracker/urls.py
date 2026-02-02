# URL patterns for tracker app
from django.urls import path
from . import views

# define url patterns
urlpatterns = [
    path('', views.home, name='home'),  # home page
    path('register/', views.register, name='register'),  # registration page
    path('logout/', views.logout_view, name='logout'),  # logout url
    path('moods/', views.mood_list, name='mood_list'),  # mood entries list
]
