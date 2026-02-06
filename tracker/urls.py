from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('mood/', views.mood_list, name='mood_list'),
    path('mood/trends/', views.mood_trends, name='mood_trends'),
    path('mood/add/', views.mood_create, name='mood_create'),
    path('mood/<int:pk>/edit/', views.mood_edit, name='mood_edit'),
    path('mood/<int:pk>/delete/', views.mood_delete, name='mood_delete'),
]
