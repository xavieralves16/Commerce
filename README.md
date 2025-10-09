# Commerce Auctions Platform

## Overview
Commerce is a Django-based web application for managing online auctions. It allows registered users to create auction listings, place bids, comment on listings, and maintain a personalized watchlist. Listings can be organized by category and closed by their owners to determine the winner based on the highest bid at the time of closing.

## Features
- **User authentication**: Register, log in, and log out using Django's built-in authentication backed by a custom `User` model.
- **Auction listings**: Create listings with titles, descriptions, starting bids, optional images, and categories. Listings remain active until their owner closes them.
- **Bidding system**: Submit bids that must exceed the current highest bid. The current price updates dynamically based on the highest bid placed.
- **Comments**: Discuss listings with other users via a comment thread displayed on each listing page.
- **Watchlist**: Add or remove listings from a personal watchlist to track auctions of interest.
- **Categories**: Browse listings by category to discover relevant auctions quickly.

## Tech Stack
- Python 3.8+
- Django 3.0.2
- SQLite (default development database)
- HTML templates styled with Bootstrap (via CDN)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/xavieralves16/Commerce.git
cd Commerce
```

### 2. Create and activate a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
Install Django directly since the project does not ship with a `requirements.txt` file:
```bash
pip install "Django==3.0.2"
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (optional but recommended)
```bash
python manage.py createsuperuser
```
This account lets you access the Django admin site at `/admin/` to manage users, listings, bids, and comments.

### 6. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to explore the application.

## Project Structure
```
Commerce/
├── auctions/              # Core app containing models, views, templates, and static assets
│   ├── models.py          # Custom User model plus Listing, Bid, and Comment models
│   ├── views.py           # Views for authentication, listing management, bidding, watchlist, and categories
│   ├── templates/         # HTML templates for the user interface
│   └── urls.py            # App-specific URL routes
├── commerce/              # Project configuration (settings, URLs, WSGI/ASGI)
├── manage.py              # Django project management script
└── README.md              # Project documentation
```

## Data Model
- `User`: Extends Django's `AbstractUser` and adds a many-to-many relationship to `Listing` for watchlists.
- `Listing`: Represents an auction listing with metadata such as starting bid, category, owner, and winner.
- `Bid`: Stores bids placed by users on listings and enforces ordering to determine the current highest bid.
- `Comment`: Tracks discussion messages associated with listings.
