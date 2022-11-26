from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Follow, Like, Comment, Dislike
from .forms import PostForm, CommentForm

def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            postContent = form.cleaned_data["postContent"]
            post = Post(postBy=request.user, postContent=postContent)
            post.save()
            return HttpResponseRedirect(reverse("network:index"))
    form = PostForm()
    posts_all = Post.objects.all().order_by('-postTime')
    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    # print(f"page is{page_number}")
    posts = paginator.get_page(page_number)
    context = {'posts': posts, 
    'likes': Like.objects.all(), 'dislikes': Dislike.objects.all(), 
    'comments': Comment.objects.all(),
    'form': form}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

def profile(request, pk):
    followValue = None
    if request.user.is_authenticated:
        followValue = Follow.objects.filter(follower=request.user, following=User.objects.get(pk=pk)).exists()
    followersCount = Follow.objects.filter(following=User.objects.get(pk=pk)).count()
    followingCount = Follow.objects.filter(follower=User.objects.get(pk=pk)).count()
    if request.method == "POST" and request.user.is_authenticated:
        if request.user != User.objects.filter(pk=pk):
            if followValue:
                Follow.objects.get(follower=request.user, following=User.objects.get(pk=pk)).delete()
                # print("Unfollowed")
            else:
                follow = Follow(follower=request.user, following=User.objects.get(pk=pk))
                follow.save()
                # print("followed")
            return HttpResponseRedirect(reverse("network:profile", args=(pk,)))

    profilePerson = User.objects.get(pk=pk)
    context = {'profilePerson': profilePerson, 
    'posts': Post.objects.filter(postBy=profilePerson).order_by('-postTime'),
    'followValue': followValue,
    'followersCount': followersCount,
    'followingCount': followingCount}
    return render(request, "network/profile.html", context)

@login_required
def following(request):
    currentUser = request.user
    following = Follow.objects.filter(follower=currentUser)
    listOfFollowing = []
    for follow in following:
        listOfFollowing.append(follow.following)
    posts_all = Post.objects.filter(postBy__in=listOfFollowing).order_by('-postTime')
    paginator = Paginator(posts_all, 10)
    page_number = request.GET.get('page')
    # print(f"page is{page_number}")
    posts = paginator.get_page(page_number)
    context = {'posts': posts}
    return render(request, "network/following.html", context)

@login_required
@csrf_exempt
def likes(request, pk):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        user = request.user
        if Like.objects.filter(likeOnPost=post, likeByUser=user).exists():
            Like.objects.get(likeOnPost=post, likeByUser=user).delete()
            message = "Like removed"
        else:
            like = Like(likeOnPost=post, likeByUser=user)
            like.save()
            message = "Like added"
        likesCount = Like.objects.filter(likeOnPost=post).count()
        return JsonResponse({"message": message, "likesCount": likesCount}, status=201)

@login_required
@csrf_exempt
def dislikes(request, pk):
    if request.method == "POST":
        post = Post.objects.get(pk=pk)
        user = request.user
        if Dislike.objects.filter(dislikeOnPost=post, dislikeByUser=user).exists():
            Dislike.objects.get(dislikeOnPost=post, dislikeByUser=user).delete()
            message = "Disliked removed"
        else:
            dislike = Dislike(dislikeOnPost=post, dislikeByUser=user)
            dislike.save()
            message = "dislike added"
        dislikesCount = Dislike.objects.filter(dislikeOnPost=post).count()
        return JsonResponse({"message": message, "dislikesCount": dislikesCount}, status=201)

@login_required
@csrf_exempt
def editPost(request, pk):
    if request.method == "PUT":
        post = Post.objects.get(pk=pk)
        # old content
        postContent = post.postContent
        # change content only after verifying user at the server side
        if post.postBy == request.user:
            data = json.loads(request.body)
            postContent = data.get("postContent")
            post.postContent = postContent
            post.save()
        return JsonResponse({"message": "Post edited", "postContent": postContent}, status=201)