from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import MoodEntry


class MoodEntryModelTest(TestCase):

	def setUp(self):
		# create a test user
		self.user = User.objects.create_user(
			username='testuser',
			password='testpass123'
		)

	def test_create_mood_entry(self):
		# test creating a mood entry
		mood = MoodEntry.objects.create(
			user=self.user,
			mood_score=7,
			notes='Feeling good today'
		)
		self.assertEqual(mood.mood_score, 7)
		self.assertEqual(mood.notes, 'Feeling good today')

	def test_mood_entry_str(self):
		# test the string representation
		mood = MoodEntry.objects.create(
			user=self.user,
			mood_score=5
		)
		self.assertIn('testuser', str(mood))
		self.assertIn('5', str(mood))

	def test_mood_ordering(self):
		# test that moods are ordered by date descending
		mood1 = MoodEntry.objects.create(user=self.user, mood_score=3)
		mood2 = MoodEntry.objects.create(user=self.user, mood_score=8)
		# ensure different dates for deterministic ordering
		mood1.date = mood1.date.replace(day=mood1.date.day - 1)
		mood1.save(update_fields=['date'])
		moods = MoodEntry.objects.all()
		# newest should be first
		self.assertEqual(moods[0], mood2)
