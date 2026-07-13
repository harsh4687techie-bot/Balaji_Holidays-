from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.conf import settings
from .models import Destination
from recommendations.models import HiddenGem


def destination_search_view(request):
    """Destination search with filtering and sorting."""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'popular')

    destinations = Destination.objects.all()

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__icontains=query)
        )

    if category and category != 'All':
        destinations = destinations.filter(categories__icontains=category)

    sort_map = {
        'popular': '-is_popular',
        'rating': '-rating',
        'price_low': 'price_per_person',
        'price_high': '-price_per_person',
        'featured': '-is_featured',
    }
    destinations = destinations.order_by(sort_map.get(sort, '-is_popular'))

    categories = ['All', 'City', 'Nature', 'Beach', 'Culture', 'Adventure', 'Food', 'Shopping', 'Wildlife', 'Mountain', 'Island']

    context = {
        'destinations': destinations,
        'query': query,
        'active_category': category or 'All',
        'active_sort': sort,
        'categories': categories,
        'total_count': destinations.count(),
    }
    return render(request, 'destinations/search.html', context)


def destination_detail_view(request, pk):
    """Detailed view of a single destination."""
    destination = get_object_or_404(Destination, pk=pk)
    hidden_gems = HiddenGem.objects.filter(destination=destination)
    related = Destination.objects.filter(
        categories__icontains=destination.get_categories()[0] if destination.get_categories() else ''
    ).exclude(pk=pk)[:4]

    context = {
        'destination': destination,
        'hidden_gems': hidden_gems,
        'related_destinations': related,
    }
    return render(request, 'destinations/detail.html', context)


def map_view(request):
    """Map view of all destinations and hidden gems."""
    destinations = Destination.objects.all().values(
        'id', 'name', 'country', 'latitude', 'longitude', 'image_url', 'rating', 'price_per_person'
    )
    gems = HiddenGem.objects.all().values(
        'id', 'name', 'latitude', 'longitude', 'image_url', 'rating'
    )

    import json
    context = {
        'destinations_json': json.dumps(list(destinations)),
        'gems_json': json.dumps(list(gems)),
        'maps_api_key': settings.MAPS_API_KEY,
    }
    return render(request, 'destinations/map.html', context)
