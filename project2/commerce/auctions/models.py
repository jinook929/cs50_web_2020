from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import IntegerField
from django.utils import timezone

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username} [ID#{self.id}]"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=50)
    bidcount = models.IntegerField(default=0)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    category = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watched = models.ManyToManyField(User, blank=True, related_name="watching")

    def __str__(self):
        return f"Listing: {self.name} [{self.lister.username}]"


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
        return f"{self.commenter.username} commented on {self.item}"
