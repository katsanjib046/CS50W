from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    listing_name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    starting_bid = models.FloatField()
    image = models.ImageField(upload_to="./auctions/static/auctions/images",default= "./auctions/static/auctions/images/on_sale.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    current_bid = models.FloatField(null=True)

    def __str__(self):
        return f"Selling {self.listing_name} by @{self.seller} starting at ${self.starting_bid} with current at ${self.current_bid}"

    def change_current_bid(self, value):
        self.current_bid = value

class Bid(models.Model):
    bid_on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_item")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_at = models.DateTimeField(auto_now_add=True)
    bid_updated_at = models.DateTimeField(auto_now=True)
    bid_amount = models.FloatField()

    def __str__(self):
        return f"Bid on {self.bid_on.listing_name} for ${self.bid_amount} on {self.bid_at} by @{self.bidder}"

class Comment(models.Model):
    comment_on = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_item_comment")
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)
    comment_update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.comment_on.listing_name} by @{self.comment_by} on {self.comment_at}"

class Watchlist(models.Model):
    watcher = models.OneToOneField(User, on_delete=models.PROTECT)
    watched_item = models.ManyToManyField(Listing)

    def __str__(self):
        return f"Watchlist for {self.watcher.username}"


