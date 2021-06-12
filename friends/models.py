import friends
from django.db import models
from login.models import *
# Create your models here.

def get_user_friends(user_id):
    user = User.objects.get(id=user_id)
    return user.friends.all()

def get_user_nonfriends(user_id):
    strangers = User.objects.exclude(friends__id=user_id).exclude(id=user_id)
    return strangers

def add(user_id, added_id):
    user = User.objects.get(id=user_id)
    added_user = User.objects.get(id=added_id)
    user.friends.add(added_user)

def remove(user_id, removed_id):
    user = User.objects.get(id=user_id)
    removed_user = User.objects.get(id=removed_id)
    user.friends.remove(removed_user)