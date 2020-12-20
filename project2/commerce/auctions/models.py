from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField


class User(AbstractUser):
    
    def __str__(self):
        return f"Username: {self.username}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    created_at = models.DateTimeField(auto_now_add=True)
    watched = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")

    def __str__(self):
        return f"Listing: {self.name}"


class Bid(models.Model):
    amount = models.IntegerField()
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="biddedListing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return f"Bid on {self.item}: ${self.amount} by {self.bidder}"


class Comment(models.Model):
    content = models.CharField(max_length=255)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentedListing")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")

    def __str__(self):
        return f"{self.commenter} commented on {self.item}"
