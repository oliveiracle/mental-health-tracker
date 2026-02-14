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

    def test_passwords_do_not_match(self):
        # test form with non-matching passwords
        data = {
            'username': 'user2',
            'email': 'user2@email.com',
            'password1': 'testpass123!',
            'password2': 'differentpass!'
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_duplicate_username(self):
        # test form with duplicate username
        RegisterForm(data={
            'username': 'userdup',
            'email': 'dup@email.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }).save()
        data = {
            'username': 'userdup',
            'email': 'other@email.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


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

    def test_invalid_mood_score(self):
        # test mood_score out of range
        data = {'mood_score': 15}
        form = MoodEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('mood_score', form.errors)

    def test_notes_too_long(self):
        # test notes exceeding maxlength
        data = {
            'mood_score': 5,
            'notes': 'a' * 600
        }
        form = MoodEntryForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('notes', form.errors)
