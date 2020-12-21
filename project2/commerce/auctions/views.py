from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from .forms import ListingForm


def index(request):
    useritems = []
    username = request.user.username
    
    print(f"Logged in as {request.user.username}")
    for object in Listing.objects.all():
        lister = object.lister.username
        if lister == username:            
            useritems.append(object)
            print(f"{object} added")

    print(useritems)
    return render(request, "auctions/index.html", {
        "listings": useritems,
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

def newListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        newlisting = form.save(commit=False)
        user = User.objects.get(username=request.user.username)
        newlisting.lister = user
        newlisting.save()
        
        return redirect('index')

    return render(request, "auctions/newListing.html", {
        'form': ListingForm(),
    })