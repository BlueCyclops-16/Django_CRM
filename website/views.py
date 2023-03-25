from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def home(request):

    # Check to see if user is trying to log in
    if request.method == 'POST':

        # Capture the data
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There was an error. Please try again.")

    return render(request, 'website/home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('home')


def register_user(request):
    return render(request, 'website/register.html', {})
