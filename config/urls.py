# main URL configuration for entire project
from django.contrib import admin
from django.urls import path, include

# url patterns for whole site
urlpatterns = [
    path('admin/', admin.site.urls),  # admin panel url
    # built-in auth urls (login, etc)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('tracker.urls')),  # include tracker app urls
]

# custom error page handlers
handler404 = 'tracker.views.handler404'
handler500 = 'tracker.views.handler500'
