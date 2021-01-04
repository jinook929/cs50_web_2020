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
    if not request.user.username:
        return render(request, "auctions/index.html")
    # tmp = User.objects.get(username=user)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.order_by("-created_at").exclude(lister=User.objects.get(username=request.user.username)).all(),
        "message": "Active Listings",
    })


@login_required(login_url='login')
def mylistings(request):
    useritems = []
    username = request.user.username
    for object in Listing.objects.order_by("-created_at").all():
        lister = object.lister.username
        if lister == username:            
            useritems.append(object)

    return render(request, "auctions/index.html", {
        "listings": useritems,
        "message": "My Listings",
    })


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
                "message": "Passwords must match.",
                'form': RegisterForm(),
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
        return render(request, "auctions/register.html", {
            'form': RegisterForm(),
        })


def newListing(request):
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
        
        return redirect('mylistings')

    return render(request, "auctions/newListing.html", {
        'form': ListingForm(),
    })

