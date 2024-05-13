from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from recipes.views import menu

from .forms import LoginUserForm, RegistrationUserForm


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginUserForm()
    data = {
        'form': form,
        'menu': menu
    }
    return render(request, 'users/login.html', context=data)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/registration_done.html')
    else:
        form = RegistrationUserForm()
    data = {
        'form': form,
        'menu': menu
    }
    return render(request, 'users/registration.html', context=data)

