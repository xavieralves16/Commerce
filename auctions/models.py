from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.FloatField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", null=True, blank=True)
    def __str__ (self):
        return f"{self.title} ({self.id})"
    
class Bid(models.Model):
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.amout} by {self.bidder} on {self.listing}"
    
class Comment(models.Model):
    content = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.content} by {self.commenter} on {self.listing}"
    


