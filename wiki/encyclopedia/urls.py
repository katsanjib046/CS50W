from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("random", views.random_page, name="random"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
]
