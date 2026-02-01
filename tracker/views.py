# importing necessary modules for views
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm


# home page view
def home(request):
    # just render the home template
    return render(request, 'tracker/home.html')


# register new user view
def register(request):
    if request.method == 'POST':  # if form is submitted
        form = RegisterForm(request.POST)  # get form data
        if form.is_valid():  # check if form is valid
            user = form.save()  # save new user to database
            login(request, user)  # automatically log in the new user
            # show success message
            messages.success(
                request,
                f"Welcome {user.username}! Your account has been created.",
            )
            return redirect('home')  # go to home page
    else:  # if GET request (just loading the page)
        form = RegisterForm()  # create empty form
    
    # add bootstrap classes to make form look nice
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    # render register template with form
    return render(request, 'tracker/register.html', {'form': form})


# logout view
def logout_view(request):
    logout(request)  # logout user
    # show message
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # return to home page
