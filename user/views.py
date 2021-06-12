from django.shortcuts import render
from . import models
# Create your views here.

def show_user(request, id):
    context = {
        'user': models.User.objects.get(id=id),
    }
    return render(request, 'user.html', context)