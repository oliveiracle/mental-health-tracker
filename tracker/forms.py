from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MoodEntry


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap 'form-control' class to all fields for consistent styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                "class": "form-control",
            })
            # Remove 'aria-describedby' if present to avoid duplicate hints
            if hasattr(self.fields[field_name].widget, 'attrs'):
                self.fields[field_name].widget.attrs.pop('aria-describedby', None)


class MoodEntryForm(forms.ModelForm):
    mood_score = forms.IntegerField(
        min_value=0,
        max_value=10,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "type": "range",      # HTML5 range slider
                "min": "0",
                "max": "10",
                "step": "1",
                "class": "form-range", # Bootstrap slider class
                "value": "5",         # Default value
            }
        ),
    )
    notes = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control", # Bootstrap textarea class
                "rows": "6",
                "maxlength": "500",
                "placeholder": (
                    "E.g.: Slept little, lots of work, "
                    "but managed to go for a walk."
                ),
            }
        ),
    )

    class Meta:
        model = MoodEntry
        fields = ['mood_score', 'notes']
