from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Comment

class NewCreateForm(forms.Form):
    categories = []
    categories.append(("none", "None")) # value, display
    for cat in Category.objects.all():
        categories.append((cat.id, cat))

    title = forms.CharField(label='Listing Title')
    description = forms.CharField(label='Description')
    bid = forms.DecimalField(label='Starting Bid')
    url = forms.URLField(label='image', required=False)
    category = forms.ChoiceField(choices=categories, required=False)

class NewCommentForm(forms.Form):
    comment = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Leave a comment'}))

class NewBidForm(forms.Form):
    # class Meta:
    #     model = Listing
    #     fields = ["currBid"]

    bid = forms.DecimalField(label='Bid', widget=forms.TextInput(attrs={'placeholder': 'Bid'}))

    def __init__(self, *args, **kwargs):
        self.currBid = kwargs.pop('currBid', None)
        super(NewBidForm, self).__init__(*args, **kwargs)

    def clean(self):
        # super(NewBidForm, self).clean()

        bid = self.cleaned_data.get('bid')

        if bid <= self.currBid:
            # print("Error found!")
            # self._errors['bid'] = self.error_class([
            #     'Minimum bid has to be be greater than the current bid!'
            # ])
            # raise forms.ValidationError("Please enter a bid higher than the current bid!")
            raise forms.ValidationError({'bid': ["Minimum bid has to be be greater than the current bid!"]})
        return self.cleaned_data

# displays Active Listing
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

# log in user
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

# log out user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# register new user
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
 
def create(request):
    if request.method == "POST":
        form = NewCreateForm(request.POST)
        if form.is_valid():
            title_ = form.cleaned_data["title"]
            description_ = form.cleaned_data["description"]
            bid_ = form.cleaned_data["bid"]
            url_ = form.cleaned_data["url"]
            category_ = form.cleaned_data["category"]
            print("Category: " + category_)
            print(type(category_))
            if category_ == "none":
                category_ = None
            else:
                category_ = Category.objects.get(pk=category_)
            print("Curr URL: ", url_)
            if not url_:
                url_ = 'https://t4.ftcdn.net/jpg/05/24/79/53/360_F_524795399_deNrm5E4w2YDrx0JRP8mTe89ghUMvIoC.jpg'
            print("URL: ", url_)
    
            newListing = Listing(title=title_, description=description_, bid=bid_, image=url_, category=category_, seller=request.user)
            newListing.save()
                        
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": NewCreateForm()
    })

def details(request, item):
    if request.method == "POST":
        listing = Listing.objects.get(pk=item)
        
        form = NewBidForm(request.POST, currBid=listing.bid)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            bidder = request.user

            listing.bid = bid
            listing.buyer = bidder
            listing.numBids += 1
            listing.save()
                        
            return HttpResponseRedirect(reverse("listing", args=(item,)))
        else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=item),
                "form": form,
                "form2": NewCommentForm()
            })

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=item),
        "form": NewBidForm(),
        "form2": NewCommentForm()
    })

def watchlist(request, item, action):
    if request.method == "POST":

        listing = Listing.objects.get(pk=item) # item we're currently on
        currUser = request.user # user whose watchlist we're trying to add to
        if action == "add":
            listing.watching.add(currUser)
        else:
            listing.watching.remove(currUser)

        return HttpResponseRedirect(reverse("listing", args=(item,)))

def closeBid(request, item):
    if request.method == "POST":

        listing = Listing.objects.get(pk=item) # item we're currently on
        currUser = request.user # user whose watchlist we're trying to add to
        
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(item,)))

def userWatchlist(request, userNum):
    user = User.objects.get(pk=userNum)

    return render(request, "auctions/watchlist.html")

def category(request):
    listCat = Category.objects.all()

    return render(request, "auctions/category.html", {
        "cats": listCat
    })

def categoryListings(request, catId):
    return render(request, "auctions/categoryListings.html", {
        "cat": Category.objects.get(pk=catId),
        "listing": Listing.objects.all()
    })

def comment(request, item):
    if request.method == "POST":
        listing_ = Listing.objects.get(pk=item)
        
        form2 = NewCommentForm(request.POST)
        if form2.is_valid():
            comment_ = form2.cleaned_data["comment"]
            commenter_ = request.user

            newCom = Comment(comment=comment_, user=commenter_, listing=listing_)
            newCom.save()
                        
            return HttpResponseRedirect(reverse("listing", args=(item,)))
        else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=item),
                "form": NewBidForm(),
                "form2": form2
            })

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=item),
        "form": NewBidForm(),
        "form2": NewCommentForm()
    })