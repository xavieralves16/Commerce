from django.contrib import admin
from .models import User, Listing, Bid, Comment

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "owner", "is_active", "created_at")
    list_filter = ("is_active", "category", "created_at")
    search_fields = ("title", "description", "owner__username", "category")
    ordering = ("-created_at",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "bidder", "listing", "created_at")
    list_filter = ("created_at",)
    search_fields = ("bidder__username", "listing__title")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter", "listing", "content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("commenter__username", "listing__title", "content")
    ordering = ("-created_at",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser")