from django.test import TestCase
from tracker.forms import RegisterForm, MoodEntryForm


class RegisterFormTest(TestCase):

    def test_valid_form(self):
        # test form with valid data
        data = {
            'username': 'newuser',
            'email': 'test@email.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        # test form with invalid email
        data = {
            'username': 'newuser',
            'email': 'not-an-email',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())


class MoodEntryFormTest(TestCase):

    def test_valid_mood_form(self):
        # test mood form with valid data
        data = {
            'mood_score': 7,
            'notes': 'Good day'
        }
        form = MoodEntryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_mood_without_notes(self):
        # notes are optional
        data = {
            'mood_score': 5
        }
        form = MoodEntryForm(data=data)
        self.assertTrue(form.is_valid())
