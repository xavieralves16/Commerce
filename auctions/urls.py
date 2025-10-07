from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("whatchlist", views.watchlist_view, name="watchlist"),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<str:category_name>/", views.categories_view, name="category_listings"),
]
