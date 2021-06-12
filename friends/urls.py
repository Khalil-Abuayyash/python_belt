from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_friends),
    path('add_friend/<int:added_id>', views.add_friend),
    path('remove_friend/<int:removed_id>', views.remove_friend),
]