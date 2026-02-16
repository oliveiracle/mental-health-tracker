from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserFlowIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_complete_user_flow(self):
        # Login
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)

        # Create mood entry
        mood_data = {'mood_score': 7, 'notes': 'Feeling good'}
        response = self.client.post(reverse('mood_create'), mood_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation

        # View mood list
        response = self.client.get(reverse('mood_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Feeling good')

        # Edit mood entry (assuming mood id = 1 for test)
        edit_data = {'mood_score': 8, 'notes': 'Feeling better'}
        response = self.client.post(reverse('mood_edit', args=[1]), edit_data)
        self.assertEqual(response.status_code, 302)

        # Delete mood entry
        response = self.client.post(reverse('mood_delete', args=[1]))
        self.assertEqual(response.status_code, 302)

        # Confirm deletion
        response = self.client.get(reverse('mood_list'))
        self.assertNotContains(response, 'Feeling better')
