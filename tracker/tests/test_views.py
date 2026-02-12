from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import MoodEntry


class HomeViewTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class MoodListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(response.status_code, 200)


class MoodCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()

    def test_can_create_mood(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('mood_create'), {
            'mood_score': 7,
            'notes': 'Test note'
        })
        self.assertEqual(MoodEntry.objects.count(), 1)
