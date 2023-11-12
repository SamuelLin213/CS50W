from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # default path for tasks
    path("add", views.add, name="add") # add path
]
