from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """In addition to abstract User, add an avatar field."""
    avatar = models.ImageField(upload_to="avatars", default="avatars/avatar.png")

class Post(models.Model):
    """This object represents a post."""
    postBy = models.ForeignKey(User, on_delete=models.CASCADE)
    postContent = models.CharField(max_length=1000)
    postTime = models.DateTimeField(auto_now_add=True)
    # postLikes = models.IntegerField(default=0)
    # postDislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.postBy} posted {self.postContent} at {self.postTime}"

class Follow(models.Model):
    """This object represents a follow."""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    folowTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"

class Comment(models.Model):
    """This object represents a comment."""
    commentOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentByUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.CharField(max_length=1000)
    commentTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commentByUser} commented {self.commentText} at {self.commentTime}"

class Like(models.Model):
    """This object represents a like."""
    likeOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    likeByUser = models.ForeignKey(User, on_delete=models.CASCADE)
    likeTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.likeByUser} liked {self.likeOnPost} at {self.likeTime}"

class Dislike(models.Model):
    """This object represents a dislike."""
    dislikeOnPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    dislikeByUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dislikeTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dislikeByUser} disliked {self.dislikeOnPost} at {self.dislikeTime}"
