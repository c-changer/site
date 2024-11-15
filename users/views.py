from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('partners')  # Replace 'home' with your home URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/sign-up.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        redirect('partners')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_authenticated:
            login(request, user)
            return redirect('partners')  # Replace 'home' with your home URL
        else:
            return render(request, 'users/sign-in.html', {"error":"error"})
    return render(request, 'users/sign-in.html')

def user_logout(request):
    logout(request)
    return redirect('sign-in')  # Replace 'home' with your home URL
