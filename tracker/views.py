from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from .forms import RegisterForm, MoodEntryForm
from .models import MoodEntry, Resource


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
            return redirect('mood_list')
    else:
        form = RegisterForm()

    # bootstrap styling
    for field in form.fields.values():
        existing_classes = field.widget.attrs.get('class', '')
        if 'form-range' in existing_classes:
            field.widget.attrs['class'] = existing_classes
        else:
            field.widget.attrs['class'] = (
                f"{existing_classes} form-control".strip()
            )

    return render(request, 'tracker/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def mood_list(request):
    # get all moods for current user, ordered by date (newest first)
    all_moods = MoodEntry.objects.filter(user=request.user)
    
    # set up paginator: 10 moods per page
    paginator = Paginator(all_moods, 10)
    page_number = request.GET.get('page')
    moods = paginator.get_page(page_number)
    
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
        existing_classes = field.widget.attrs.get('class', '')
        if 'form-range' in existing_classes:
            field.widget.attrs['class'] = existing_classes
        else:
            field.widget.attrs['class'] = (
                f"{existing_classes} form-control".strip()
            )
    
    return render(request, 'tracker/mood_form.html', {'form': form})


@login_required
def mood_edit(request, pk):
    mood = MoodEntry.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = MoodEntryForm(request.POST, instance=mood)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mood updated!')
            return redirect('mood_list')
    else:
        form = MoodEntryForm(instance=mood)
    
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'tracker/mood_form.html', {'form': form})


@login_required
def mood_delete(request, pk):
    mood = MoodEntry.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        mood.delete()
        messages.success(request, 'Mood deleted!')
        return redirect('mood_list')
    return render(request, 'tracker/mood_confirm_delete.html', {'mood': mood})


@login_required
def mood_trends(request):
    today = timezone.localdate()
    start_date = today - timedelta(days=6)
    days = [start_date + timedelta(days=offset) for offset in range(7)]

    weekly_data = (
        MoodEntry.objects.filter(
            user=request.user, date__range=(start_date, today)
        )
        .values('date')
        .annotate(avg_score=Avg('mood_score'))
    )
    avg_map = {item['date']: item['avg_score'] for item in weekly_data}

    labels = [day.strftime('%a') for day in days]
    scores = [round(avg_map.get(day) or 0, 2) for day in days]

    weekly_avg = round(
        (sum(scores) / len([s for s in scores if s > 0]))
        if any(s > 0 for s in scores)
        else 0,
        2,
    )
    weekly_max = max(scores) if scores else 0
    weekly_min = min([s for s in scores if s > 0], default=0)

    context = {
        'labels': labels,
        'scores': scores,
        'weekly_avg': weekly_avg,
        'weekly_max': weekly_max,
        'weekly_min': weekly_min,
    }
    return render(request, 'tracker/mood_trends.html', context)


@login_required
def resource_list(request):
    categories = Resource.CATEGORY_CHOICES
    resources = Resource.objects.all().order_by('category', 'title')
    grouped_resources = {key: [] for key, _ in categories}

    for resource in resources:
        grouped_resources[resource.category].append(resource)

    sections = [
        {
            'key': key,
            'label': label,
            'items': grouped_resources.get(key, []),
        }
        for key, label in categories
    ]

    context = {
        'sections': sections,
    }
    return render(request, 'tracker/resources_list.html', context)


