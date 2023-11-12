from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #watchlist = models.ManyToManyField(Listing, blank=True, related_name="users_watching")
    def __str__(self):
        return f"{self.id}: {self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

defaultImg = 'https://t4.ftcdn.net/jpg/05/24/79/53/360_F_524795399_deNrm5E4w2YDrx0JRP8mTe89ghUMvIoC.jpg'
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=800)
    bid = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.URLField(default=defaultImg)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings", null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings", null=True)
    active = models.BooleanField(default=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_purchases", null=True)
    watching = models.ManyToManyField(User, blank=True, related_name="user_watchlist")
    numBids = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids", null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f"{self.id}: ${self.amount} by {self.user.username}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", null=True)
    comment = models.CharField(max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", null=True)

    def __str__(self):
        return f"{self.id}: {self.comment} on {self.listing.title} by {self.user.username}"