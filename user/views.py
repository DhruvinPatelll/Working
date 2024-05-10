from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, LoginForm
from django.contrib import auth


CustomUser = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('room')  
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('room') 
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('login') 
