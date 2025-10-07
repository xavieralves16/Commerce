from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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

def create_listing(request):
    if request.method == "POST":
        #Get form data
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        #Validate form data
        if not title or not description or not starting_bid:
            return render(request, "auctions/create.html", {
                "message": "Title, description, and starting bid are required."
            })
        
        try:
            starting_bid = float(starting_bid)
            if starting_bid <= 0:
                raise ValueError
        except ValueError:
            return render(request, "auctions/create.html", {
                "message": "Starting bid must be a positive number."
            })
        
        #Create new listing
        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            owner=request.user,
            is_active=True
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")
    
def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user

    current_bid = listing.current_price

    in_watchlist = user.is_authenticated and listing in user.watchlist.all()

    if request.method == "POST":
        if not user.is_authenticated:
            messages.error(request, "You must be logged in to perform this action.")
            return redirect("login")

        #Add or remove from watchlist
        if "watchlist" in request.POST:
            if in_watchlist:
                user.watchlist.remove(listing)
                messages.info(request, "Removed from watchlist.")
            else:
                user.watchlist.add(listing)
                messages.info(request, "Added to watchlist.")
            return redirect("listing", listing_id=listing.id)
        
        # Place a bid
        elif "bid" in request.POST:
            try:
                bid_amount = float(request.POST["bid_amount"])
            except ValueError:
                messages.error(request, "Invalid bid amount.")
                return redirect("listing", listing_id=listing.id)
            
            if bid_amount <= listing.current_price:
                messages.error(request, "Bid must be higher than current price.")
                return redirect("listing", listing_id=listing.id)
            
            else:
                Bid.objects.create(
                    amount=bid_amount,
                    bidder=user,
                    listing=listing
                )
                messages.success(request, "Bid placed successfully.")
                return redirect("listing", listing_id=listing.id)
        
        # Close the auction
        elif "close" in request.POST and user == listing.owner:
            if current_bid:
                listing.winner = current_bid.bidder
            listing.is_active = False
            listing.save()
            messages.info(request, "Auction closed.")
            return redirect("listing", listing_id=listing.id)
        
        # Add a comment
        elif "comment" in request.POST:
            content = request.POST["content"]
            if content:
                Comment.objects.create(
                    content=content,
                    commenter=user,
                    listing=listing
                )
                messages.success(request, "Comment added.")
            else:
                messages.error(request, "Comment cannot be empty.")
            return redirect("listing", listing_id=listing.id)
        
    coments = listing.comments.all().order_by('-created_at')

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": listing.current_price,
        "in_watchlist": in_watchlist,
        "comments": coments
    })

def watchlist_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your watchlist.")
        return redirect("login")
    
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories_view(request, category_name=None):
    if category_name:
        listings = Listing.objects.filter(is_active=True, category=category_name)
        return render(request, "auctions/category_listings.html", {
            "category": category_name,
            "listings": listings
        })
    else:
        categories = Listing.objects.values_list('category', flat=True).distinct()
        categories = [c for c in categories if c]  
        return render(request, "auctions/categories.html", {
            "categories": categories
        })
            


