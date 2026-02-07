from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MoodEntry


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# form for mood entry
class MoodEntryForm(forms.ModelForm):
    mood_score = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": "0",
                "max": "10",
                "step": "1",
                "class": "form-range",
                "value": "5",
            }
        ),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "6",
                "maxlength": "500",
                "placeholder": (
                    "Ex.: Dormi pouco, muito trabalho, mas consegui caminhar."
                ),
            }
        ),
    )

    class Meta:
        model = MoodEntry
        fields = ['mood_score', 'notes']
