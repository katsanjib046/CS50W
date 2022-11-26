
from django.urls import path

from . import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API Routes
    path("likes/<int:pk>", views.likes, name="likes"),
    path("dislikes/<int:pk>", views.dislikes, name="dislikes"),
    path("edit/<int:pk>", views.editPost, name="edit"),
]
