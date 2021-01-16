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
        "listings": Listing.objects.order_by("-created_at").all(),
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
    watchedItemsNum = 0
    try:
        watcher = User.objects.get(username=request.user.username)
        watchedItems = Listing.objects.filter(watched=watcher)
        watchedItemsNum = len(watchedItems)
    except:
        pass

    try:
        watchingUsers = User.objects.filter(watching=Listing.objects.get(id=id).id)
        print(watchingUsers)
        watchingArr = []
        for user in watchingUsers:
            watchingArr.append(user.username)
    except:
        watchingArr = []

    target = Listing.objects.get(id=id)
    try:
        startWatching = User.objects.get(username=request.user.username)
        try:
            currentUser = target.watched.all().get(username=request.user.username)
            target.watched.remove(currentUser)
        except:
            target.watched.add(startWatching)
            target.save()
    except:
        pass

    return render(request, "auctions/listing.html", {
        "item": Listing.objects.get(id=id),
        "watching": watchingArr,
        "watchedItemsNum": watchedItemsNum,
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