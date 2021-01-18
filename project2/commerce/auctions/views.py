from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from .forms import *


def index(request):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass

    context = {
        "listings": Listing.objects.order_by("-created_at").filter(is_closed=False),
        "watchedItemsNum": watchedItemsNum,
    }
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


@login_required(login_url='login')
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
                "message": "Passwords must match.",
                'form': RegisterForm(),
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                'form': RegisterForm(),
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            'form': RegisterForm(),
        })


def categories(request):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass
    context = {
        "categories": [],
        "watchedItemsNum": watchedItemsNum,
    }

    for category in CATEGORY_CHOICES:
        context["categories"].append(category[0])

    return render(request, "auctions/categories.html", context)


def categoryListings(request, category):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass
    
    listings = Listing.objects.order_by("-created_at").all().filter(category=category)
    context = {
        "categories": [],
        "category": category,
        "listings": listings,
        "watchedItemsNum": watchedItemsNum,
    }
    for category in CATEGORY_CHOICES:
        context["categories"].append(category[0])

    return render(request, "auctions/categoryListings.html", context)


def newListing(request):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass
    if request.method == "POST":

        # form = ListingForm(request.POST)
        # newlisting = form.save(commit=False)
        # user = User.objects.get(username=request.user.username)
        # newlisting.lister = user
        # newlisting.save()

        newlisting = Listing()

        if not request.POST['name'] or not request.POST['description'] or not request.POST['price']:
            return render(request, "auctions/newListing.html", {
                'form': ListingForm(),
                'submessage': "*** Fill in the required boxes ***"
            })

        newlisting.name = request.POST['name']
        newlisting.category = request.POST['category']
        newlisting.description = request.POST['description']
        newlisting.price = request.POST['price']
        try:
            newlisting.image = request.FILES['image']
        except:
            pass
        newlisting.lister = User.objects.get(username=request.user.username)
        newlisting.save()
        
        return render(request, 'auctions/listing.html', { "item": Listing.objects.get(name=newlisting.name) })

    return render(request, "auctions/newListing.html", {
        'form': ListingForm(),
        'watchedItemsNum': watchedItemsNum,
    })

def listing(request, id):
    # Decide the number of watched items by the logged-in user
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass
    
    # Retrieve watching users to find whether the logged-in user is watching
    try:
        watchingUsers = User.objects.filter(watching=Listing.objects.get(id=id).id)
        print(watchingUsers)
        watchingArr = []
        for user in watchingUsers:
            watchingArr.append(user.username)
    except:
        watchingArr = []

    # Prepare variables for the item and its comments
    target = Listing.objects.get(id=id)
    comments = Comment.objects.all().order_by("-created_at").filter(item=Listing.objects.get(id=id))

    # Update database based on bidding
    if request.method == "POST":
        try:
            bidbox = int(request.POST["bidbox"])
            message = ""
            def placeBid():
                newBid = Bid()
                newBid.amount = bidbox
                newBid.item = target
                newBid.bidder = User.objects.get(username=request.user.username)
                newBid.save()
                target.price = newBid.amount
                target.bidcount += 1
                target.lastbidding_by = request.user.username
                target.save()

            if target.bidcount == 0:
                if bidbox >= target.price:
                    placeBid()
                else:
                    message = "The first bid must be at least as large as the starting bid."            
            else: 
                if bidbox > target.price:
                    placeBid()
                else:
                    message = "New bid must be greater than the current one."

            return render(request, "auctions/listing.html", {
                "item": Listing.objects.get(id=id),
                "watching": watchingArr,
                "watchedItemsNum": watchedItemsNum,
                "comments": comments,
                "form": CommentForm(),
                "message": message,
            })
        except:
            pass

        # Update database based on closing
        if request.POST["close"]:
            target.is_closed = True
            target.winner = target.lastbidding_by
            message = f"Congratulations, {target.winner} !!! You are won this item."
            target.save()

            context = {
                "item": target,
                "watching": watchingArr,
                "watchedItemsNum": watchedItemsNum,
                "comments": comments,
                "form": CommentForm(),
                "winner": target.winner
            }
            if target.bidcount < 1:
                context["winner"] = "No one"
                return render(request, "auctions/listing.html", context)
            return render(request, "auctions/listing.html", context)
        
        # Update database based on commenting
        try:
            newComment = Comment()
            newComment.content = request.POST["comment"]
            newComment.item = target
            newComment.commenter = User.objects.get(username=request.user.username)
            newComment.save()
        except:
            pass

    return render(request, "auctions/listing.html", {
        "item": Listing.objects.get(id=id),
        "watching": watchingArr,
        "watchedItemsNum": watchedItemsNum,
        "comments": comments,
        "form": CommentForm(),
        "listerName": target.lister.username,
        "winner": target.winner
    })


def watchlist(request):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass

    context = {
        "watchedItemsNum": watchedItemsNum,
        "listings": Listing.objects.filter(watched=User.objects.get(username=request.user.username))
    }
    return render(request, 'auctions/watchlist.html', context)


def winlist(request):
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass
    
    try:
        closedListings = Listing.objects.filter(is_closed=True)
        winlistings = []
        winlistings.append(closedListings.get(winner=request.user.username))
        print(winlistings)
    except:
        print("winlistings = []")
        winlistings = []
        pass

    context = {
        "watchedItemsNum": watchedItemsNum,
        "listings": winlistings,
    }
    return render(request, 'auctions/winlist.html', context)


def watchlistToggle(request):
    context ={
        "item": Listing.objects.get(name="Yoyo")
    }
    return render(request, 'auctions/listing.html', context)


def listingsByLister(request, lister):
    username = User.objects.get(username=lister)
    context = {
        "lister": lister,
        "listings": Listing.objects.filter(lister=username).order_by("-created_at").all(),
    }
    return render(request, 'auctions/listingsByLister.html', context)

def test(request):
    items = Listing.objects.filter(is_closed=True).order_by("-created_at")    
    context = {
        "items": items,
    }
    return render(request, "auctions/test.html", context)