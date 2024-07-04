from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    # Creates logic for client signup.
    
    if request.method == 'POST':
        # Get client details from request
        email = request.POST['email']
        username = request.POST['username'] 
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Checks if passwords match
        if password == confirm_password:
            # Checks if email is present.
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
                # Checks if username is present.
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                # Creates new user
                user = User.objects.create_user(email=email, username=username, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:  
        return render(request, 'signup.html')

@login_required(login_url='login')
def login(request):
    # Creates logic for client login.
    if request.method == 'POST':
        # Get client details from request
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user
        user = auth.authenticate(username=username, password=password)
        # Check if user exists
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Check your credentials')
            return redirect('login')
    return render(request, 'login.html')