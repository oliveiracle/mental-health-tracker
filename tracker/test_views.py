from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import MoodEntry, Resource


class HomeViewTest(TestCase):
    """Tests for the home page view."""

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/home.html')


class RegisterViewTest(TestCase):
    """Tests for user registration view."""

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/register.html')

    def test_register_valid_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@email.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_invalid_data_stays_on_page(self):
        data = {
            'username': '',
            'email': 'bad',
            'password1': 'a',
            'password2': 'b',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    """Tests for the logout view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_logout_redirects_to_home(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class MoodListViewTest(TestCase):
    """Tests for the mood list view including auth and pagination."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_user_can_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/mood_list.html')

    def test_user_only_sees_own_moods(self):
        other_user = User.objects.create_user(
            username='otheruser', password='testpass123'
        )
        MoodEntry.objects.create(
            user=other_user, mood_score=3, notes='Other user mood'
        )
        MoodEntry.objects.create(
            user=self.user, mood_score=7, notes='My mood'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_list'))
        self.assertContains(response, 'My mood')
        self.assertNotContains(response, 'Other user mood')

    def test_pagination_shows_max_10(self):
        self.client.login(username='testuser', password='testpass123')
        for i in range(15):
            MoodEntry.objects.create(
                user=self.user, mood_score=5, notes=f'Entry {i}'
            )
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(len(response.context['moods']), 10)

    def test_pagination_page_2(self):
        self.client.login(username='testuser', password='testpass123')
        for i in range(15):
            MoodEntry.objects.create(
                user=self.user, mood_score=5, notes=f'Entry {i}'
            )
        response = self.client.get(reverse('mood_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['moods']), 5)


class MoodCreateViewTest(TestCase):
    """Tests for creating a mood entry."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mood_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/mood_form.html')

    def test_create_valid_mood(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'mood_score': 7, 'notes': 'Great day'}
        response = self.client.post(reverse('mood_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MoodEntry.objects.count(), 1)
        self.assertEqual(MoodEntry.objects.first().user, self.user)

    def test_create_invalid_mood_stays_on_page(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'mood_score': 15}
        response = self.client.post(reverse('mood_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MoodEntry.objects.count(), 0)


class MoodEditViewTest(TestCase):
    """Tests for editing a mood entry including permission checks."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.mood = MoodEntry.objects.create(
            user=self.user, mood_score=5, notes='Original'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('mood_edit', args=[self.mood.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('mood_edit', args=[self.mood.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_valid_data(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'mood_score': 9, 'notes': 'Updated'}
        response = self.client.post(
            reverse('mood_edit', args=[self.mood.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.mood.refresh_from_db()
        self.assertEqual(self.mood.mood_score, 9)
        self.assertEqual(self.mood.notes, 'Updated')

    def test_cannot_edit_other_users_mood(self):
        other_user = User.objects.create_user(
            username='otheruser', password='testpass123'
        )
        other_mood = MoodEntry.objects.create(
            user=other_user, mood_score=3
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('mood_edit', args=[other_mood.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_nonexistent_mood_returns_404(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_edit', args=[9999]))
        self.assertEqual(response.status_code, 404)


class MoodDeleteViewTest(TestCase):
    """Tests for deleting a mood entry including permission checks."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.mood = MoodEntry.objects.create(
            user=self.user, mood_score=5, notes='To delete'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('mood_delete', args=[self.mood.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_confirmation_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('mood_delete', args=[self.mood.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'tracker/mood_confirm_delete.html'
        )

    def test_delete_mood_entry(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('mood_delete', args=[self.mood.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MoodEntry.objects.count(), 0)

    def test_cannot_delete_other_users_mood(self):
        other_user = User.objects.create_user(
            username='otheruser', password='testpass123'
        )
        other_mood = MoodEntry.objects.create(
            user=other_user, mood_score=3
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('mood_delete', args=[other_mood.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(MoodEntry.objects.filter(pk=other_mood.pk).exists())

    def test_delete_nonexistent_mood_returns_404(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('mood_delete', args=[9999])
        )
        self.assertEqual(response.status_code, 404)


class MoodTrendsViewTest(TestCase):
    """Tests for the mood trends view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mood_trends'))
        self.assertEqual(response.status_code, 302)

    def test_trends_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_trends'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/mood_trends.html')

    def test_trends_context_has_required_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_trends'))
        self.assertIn('labels', response.context)
        self.assertIn('scores', response.context)
        self.assertIn('weekly_avg', response.context)
        self.assertIn('weekly_max', response.context)
        self.assertIn('weekly_min', response.context)
        self.assertEqual(len(response.context['labels']), 7)
        self.assertEqual(len(response.context['scores']), 7)

    def test_trends_with_no_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('mood_trends'))
        self.assertEqual(response.context['weekly_avg'], 0)
        self.assertEqual(response.context['weekly_max'], 0)


class ResourceListViewTest(TestCase):
    """Tests for the resource list view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('resource_list'))
        self.assertEqual(response.status_code, 302)

    def test_resource_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('resource_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/resources_list.html')

    def test_resources_grouped_by_category(self):
        self.client.login(username='testuser', password='testpass123')
        Resource.objects.create(
            title='Test ADHD',
            description='Desc',
            link='http://example.com',
            category='adhd',
        )
        response = self.client.get(reverse('resource_list'))
        sections = response.context['sections']
        self.assertEqual(len(sections), 4)
        adhd_section = next(s for s in sections if s['key'] == 'adhd')
        self.assertGreaterEqual(len(adhd_section['items']), 1)


class PrivacyViewTest(TestCase):
    """Tests for the privacy page."""

    def test_privacy_page_loads(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/privacy.html')
