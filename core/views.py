import json
from decimal import Decimal

from django.shortcuts import render
from destinations.models import Destination
from .models import FAQ
from recommendations.views import recommendation_engine


def ensure_sample_destinations():
    """Create a small set of sample destinations if the database is empty."""
    try:
        if Destination.objects.exists():
            return
    except Exception:
        return

    sample_destinations = [
        {
            'name': 'Santorini',
            'country': 'Greece',
            'description': 'A postcard-perfect island known for caldera sunsets, whitewashed villages, and romantic stays.',
            'short_description': 'Sunset views, cliffside stays, and unforgettable dinners.',
            'price_per_person': Decimal('1290.00'),
            'rating': Decimal('4.8'),
            'categories': json.dumps(['Island', 'Beach', 'Romantic']),
            'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
            'is_popular': True,
            'best_season': 'May - October',
            'language': 'Greek',
            'currency': 'EUR',
        },
        {
            'name': 'Kyoto',
            'country': 'Japan',
            'description': 'A timeless city of temples, tea houses, gardens, and seasonal festivals.',
            'short_description': 'Culture-rich streets, gardens, and traditional cuisine.',
            'price_per_person': Decimal('1180.00'),
            'rating': Decimal('4.7'),
            'categories': json.dumps(['City', 'Culture', 'Food']),
            'image_url': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
            'is_popular': True,
            'best_season': 'March - May',
            'language': 'Japanese',
            'currency': 'JPY',
        },
        {
            'name': 'Marrakech',
            'country': 'Morocco',
            'description': 'A sensory-rich destination blending souks, riads, and desert adventures.',
            'short_description': 'Colorful streets, rich food, and timeless architecture.',
            'price_per_person': Decimal('980.00'),
            'rating': Decimal('4.6'),
            'categories': json.dumps(['City', 'Culture', 'Adventure']),
            'image_url': 'https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
            'is_popular': True,
            'best_season': 'October - April',
            'language': 'Arabic',
            'currency': 'MAD',
        },
        {
            'name': 'Queenstown',
            'country': 'New Zealand',
            'description': 'A dramatic alpine playground with lakes, adventure sports, and breathtaking scenery.',
            'short_description': 'Adventure, lakeside views, and luxury lodges.',
            'price_per_person': Decimal('1450.00'),
            'rating': Decimal('4.9'),
            'categories': json.dumps(['Adventure', 'Nature', 'Scenic']),
            'image_url': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
            'is_popular': True,
            'best_season': 'December - March',
            'language': 'English',
            'currency': 'NZD',
        },
    ]

    for destination_data in sample_destinations:
        Destination.objects.create(**destination_data)


def landing_view(request):
    """Public landing page with featured destinations."""
    try:
        ensure_sample_destinations()
        featured = Destination.objects.filter(is_featured=True)[:4]
        popular = Destination.objects.filter(is_popular=True)[:6]
    except Exception:
        featured = []
        popular = []

    context = {
        'featured_destinations': featured,
        'popular_destinations': popular,
    }
    return render(request, 'core/landing.html', context)


def home_view(request):
    """Logged-in user home dashboard."""
    try:
        ensure_sample_destinations()
        featured = Destination.objects.filter(is_featured=True)[:4]
        popular = Destination.objects.filter(is_popular=True)[:8]
    except Exception:
        featured = []
        popular = []

    recommended_gems = recommendation_engine(request.user, limit=6)

    trips = []
    if request.user.is_authenticated:
        from trips.models import Trip
        try:
            trips = Trip.objects.filter(user=request.user)[:5]
        except Exception:
            trips = []

    context = {
        'featured_destinations': featured,
        'popular_destinations': popular,
        'recommended_gems': recommended_gems,
        'recent_trips': trips,
    }
    return render(request, 'core/home.html', context)


def faq_view(request):
    """Help & FAQ page with category accordion."""
    category = request.GET.get('category', '')
    faqs = FAQ.objects.all()
    if category and category != 'All':
        faqs = faqs.filter(category=category)

    # Group by category
    categories = ['General', 'Planning', 'Booking', 'Safety']
    grouped = {}
    for cat in categories:
        grouped[cat] = FAQ.objects.filter(category=cat)

    context = {
        'faqs': faqs,
        'grouped_faqs': grouped,
        'categories': ['All'] + categories,
        'active_category': category or 'All',
    }
    return render(request, 'core/faq.html', context)
