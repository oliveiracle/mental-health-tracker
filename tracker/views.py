from django.shortcuts import render


def home(request):
    """Display the homepage"""
    return render(request, 'tracker/home.html')
