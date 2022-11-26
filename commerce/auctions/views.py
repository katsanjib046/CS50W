from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import User, Listing, Bid, Comment, Category, Watchlist
from .forms import CreateListing
from django.contrib import messages


def index(request):
    # sort the query set by creation date
    context = {'listing': Listing.objects.filter(active=True).order_by('-created_at'),
    'bids':Bid.objects.all(),
    'comments': Comment.objects.all()}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        # use request.POST for data and request.FILES for files
        form = CreateListing(request.POST, request.FILES)
        if form.is_valid():
            print("valid form")
            listing_name = form.cleaned_data['listing_name']
            starting_bid = form.cleaned_data['starting_bid']
            # data = {'listing_name': listing_name, 'starting_bid': starting_bid}
            files = form.cleaned_data['image']
            description = form.cleaned_data['description']
            # handle the category here
            category = form.cleaned_data['category']
            if Category.objects.filter(name=category):
                print("Found Category")
                catg = Category.objects.get(name=category)
            else:
                print("new Category")
                catg = Category(name=category)
                catg.save()
            # handle the seller here
            seller = request.user
            # Create new listing here
            f = Listing(seller=seller, listing_name = listing_name, starting_bid = starting_bid,
                         image =files, description = description, category=catg)
            f.save()
        return redirect("index")
    form = CreateListing()
    context = {'form': form}
    return render(request, "auctions/create.html", context)

def category(request):
    categories = Category.objects.all().order_by("name")
    # you don't need to send listing because you can get listing from categories
    # by doing category.listing_set.all in html itself
    context = {'categories': categories}
    return render(request, "auctions/category.html", context)

@login_required
def listing(request, pk):
    if request.method=="POST":

        if 'bid_amount' in request.POST:
            bid_on = Listing.objects.get(id=pk)
            comments = Comment.objects.filter(comment_on=bid_on)
            bid_amount = float(request.POST['bid_amount'])
            bidder = request.user

            # check if the bid is correct amount
            if current:=bid_on.current_bid:
                if bid_amount < current:
                    bids = Bid.objects.filter(bid_on=bid_on)
                    context = {'bids': bids,'item': bid_on, 'message_w':'Bid should be greater than Current bid!', 'comments':comments}
                    return render(request, "auctions/listing.html", context=context)
            else:
                if bid_amount < bid_on.starting_bid:
                    bids = Bid.objects.filter(bid_on=bid_on)
                    context = {'bids':bids, 'item': bid_on, 'message_w':'Bid should be greater than Starting bid!', 'comments':comments}
                    return render(request, "auctions/listing.html", context=context)
            bid = Bid(bid_on=bid_on, bid_amount=bid_amount, bidder=bidder)
            bid.save()
            bid_on.change_current_bid(bid_amount)
            bid_on.save()
            bids = Bid.objects.filter(bid_on=bid_on)
            if Watchlist.objects.filter(watcher = request.user):
                watched = Watchlist.objects.get(watcher = request.user).watched_item.all()
            else:
                watched = []
            context = {'bids': bids, 'item': bid_on, 'message_s': "Great! Your bid has been placed!", 'comments':comments, 'watched': watched}
            return render(request, "auctions/listing.html", context=context)
        
        elif 'newComment' in request.POST:
            comment_by = request.user
            comment_on = Listing.objects.get(id=pk)
            comment = request.POST['newComment']
            newComment = Comment(comment_by=comment_by, comment=comment, comment_on=comment_on)
            newComment.save()
            return redirect("listing", pk=pk)

        elif 'auctionClose' in request.POST:
            item = Listing.objects.get(id=pk)
            item.active = False
            item.save()
            return redirect("listing", pk=pk)

    item = Listing.objects.get(pk=pk)
    comments = Comment.objects.filter(comment_on=item)
    bids = Bid.objects.filter(bid_on=item)
    if Watchlist.objects.filter(watcher = request.user):
        watched = Watchlist.objects.get(watcher = request.user).watched_item.all()
    else:
        watched = []
    context = {'item': item, 'comments':comments, 'bids': bids, 'watched': watched}
    return render(request, "auctions/listing.html", context=context)

@login_required
def watchlist(request):
    watcher = request.user
    # if there is no watchlist for the user create it
    if not Watchlist.objects.filter(watcher=watcher):
        watch_list = Watchlist(watcher=watcher)
        watch_list.save()

    if request.method == "POST":
        if 'watchlist' in request.POST:
            item_id = int(request.POST["watchlist"])
            item = Listing.objects.get(id=item_id)
            watch_list = Watchlist.objects.get(watcher=watcher)
            watch_list.watched_item.add(item)
            watch_list.save()
        if 'watchUnlist' in request.POST:
            item_id = int(request.POST["watchUnlist"])
            item = Listing.objects.get(id=item_id)
            watch_list = Watchlist.objects.get(watcher=watcher)
            watch_list.watched_item.remove(item)
            watch_list.save()

    watch_list = Watchlist.objects.get(watcher=watcher)
    watched = watch_list.watched_item.all()
    context = {'watched': watched}
    return render(request, "auctions/watchlist.html", context)
