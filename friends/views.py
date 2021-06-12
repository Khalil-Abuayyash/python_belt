from django.shortcuts import redirect, render
from . import models

# Create your views here.

def show_friends(request):
    context = {
        'user': models.User.objects.get(id=request.session['id']),
        'friends': models.get_user_friends(request.session['id']),
        'strangers': models.get_user_nonfriends(request.session['id']),
    }
    return render(request, 'friends.html', context)

def add_friend(request, added_id):
    models.add(request.session['id'], added_id)
    return redirect('/friends')

def remove_friend(request, removed_id):
    models.remove(request.session['id'], removed_id)
    return redirect('/friends')