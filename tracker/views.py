from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, MoodEntryForm
from .models import MoodEntry


def home(request):
    return render(request, 'tracker/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome {user.username}! Account created."
            )
            return redirect('home')
    else:
        form = RegisterForm()

    # bootstrap styling
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'tracker/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def mood_list(request):
    moods = MoodEntry.objects.filter(user=request.user)
    return render(request, 'tracker/mood_list.html', {'moods': moods})


@login_required
def mood_create(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood entry added!')
            return redirect('mood_list')
    else:
        form = MoodEntryForm()
    
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'tracker/mood_form.html', {'form': form})
