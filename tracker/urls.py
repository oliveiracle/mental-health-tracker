from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('mood/', views.mood_list, name='mood_list'),
    path('mood/add/', views.mood_create, name='mood_create'),
]
