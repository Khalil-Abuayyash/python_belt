from django.contrib.messages.api import error
from django.db import models
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def main(request):
    return render(request, 'main.html')

def login(request):
    if request.method == "POST":

        if request.POST['operation'] == "login":
            errors = User.objects.validator_login(request.POST)

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            else:
                user_details = get_user_details(request.POST['email'])
                for key, value in user_details.items():
                    request.session[key] = value

                messages.success(request, "Logged in successfully")
                return redirect("/friends")

        if request.POST['operation'] == "register":
            # request.session.clear()
            errors = User.objects.validator_registeration(request.POST)
            if len(errors) > 0 :
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            else:
                create_user(request.POST)
                user_details = get_user_details(request.POST['email'])
                for key, value in user_details.items():
                    request.session[key] = value
                messages.success(request, "user successfully created")
                return redirect('/friends')
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')