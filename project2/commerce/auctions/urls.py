from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>/", views.categoryListings, name="categoryListings"),
    path("newListing/", views.newListing, name="newListing"),
    path("listings/<int:id>/", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("winlist/", views.winlist, name="winlist"),
    path("watchlistToggle/<str:item>/", views.watchlistToggle, name="watchlistToggle"),
    path("listingsByLister/<str:lister>/", views.listingsByLister, name="listingsByLister"),
    path("test/", views.test, name="test"),
]
