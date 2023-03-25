from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.


def home(request):
    # Getting all the record in Record table and assigning to records variable
    records = Record.objects.all()

    # Check to see if user is trying to log in
    if request.method == 'POST':

        # Capture the data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There was an error. Please try again.")

    return render(request, 'website/home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            # Authenticate and login just after registering
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)

            login(request, user)
            messages.success(
                request, "You Have Successfully Registered and currently Logged In")
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form': form})

    return render(request, 'website/register.html', {'form': form})


def customer_record(request, pk):

    if request.user.is_authenticated:
        customerRecord = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customerRecord': customerRecord})
    else:
        messages.success(request, "You Must be Logged In To View That Page  ")
        return redirect('home')


def delete_record(request, pk):

    if request.user.is_authenticated:
        delete_it = Record.objects.get(pk=pk)
        delete_it.delete()

        messages.success(request, "Record Deleted Successfully")
        return redirect('home')

    else:
        messages.success(
            request, "You Must be Logged In To Do This Action")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added Successfully..")
                return redirect('home')
        return render(request, 'website/addRecord.html', {'form': form})

    else:
        messages.success(request, "You Must be Logged In To Add Record")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        curr_record = Record.objects.get(id=pk)

        form = AddRecordForm(request.POST or None, instance=curr_record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record has been successfully upadted.")
            return redirect('home')
        return render(request, 'website/updateRecord.html', {'form': form})
    else:
        messages.success(request, "You Must be Logged In To Update Record")
        return redirect('home')
