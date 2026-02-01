# forms for user registration
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# custom registration form (extends django's default form)
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)  # email field (optional)

    class Meta(UserCreationForm.Meta):
        model = User  # use django User model
        # fields to show
        fields = ("username", "email", "password1", "password2")

    # save method to include email
    def save(self, commit=True):
        user = super().save(commit=False)  # get user object but don't save yet
        user.email = self.cleaned_data.get("email", "")  # add email to user
        if commit:  # if we should save to database
            user.save()  # save user
        return user  # return the user object
