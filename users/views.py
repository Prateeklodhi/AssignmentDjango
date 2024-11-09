from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Home page view for authenticated users
@login_required
def home(request):
    return render(request, 'home.html')  # You can create a 'home.html' template

# Register view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after registration
            return redirect('home')  # Redirect to a home page after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page or dashboard
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})
