from django.shortcuts import render
from django.db.models import Q
from .models import HiddenGem
from destinations.models import Destination


def hidden_gems_view(request):
    """Hidden gems discovery page with category filtering."""
    category = request.GET.get('category', '')
    destination_id = request.GET.get('destination', '')
    query = request.GET.get('q', '').strip()

    gems = HiddenGem.objects.select_related('destination').all()

    if category and category != 'All':
        gems = gems.filter(category=category)

    if destination_id:
        gems = gems.filter(destination_id=destination_id)

    if query:
        gems = gems.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(why_special__icontains=query)
        )

    categories = ['All', 'Nature', 'Culture', 'Food', 'Architecture', 'Adventure', 'Spiritual', 'Scenic']
    destinations = Destination.objects.all()

    context = {
        'gems': gems,
        'active_category': category or 'All',
        'categories': categories,
        'destinations': destinations,
        'selected_destination': destination_id,
        'query': query,
        'total_count': gems.count(),
    }
    return render(request, 'recommendations/gems.html', context)


def recommendation_engine(user, limit=6):
    """
    Server-side recommendation engine.
    Matches hidden gems and destinations to user preferences.
    Returns a queryset of recommended HiddenGems.
    """
    if not user.is_authenticated:
        return HiddenGem.objects.order_by('-rating')[:limit]

    try:
        prefs = user.preferences
        styles = prefs.get_travel_styles()
    except Exception:
        return HiddenGem.objects.order_by('-rating')[:limit]

    # Build a Q filter based on travel styles -> gem categories
    style_to_category = {
        'Adventure': 'Adventure',
        'Cultural': 'Culture',
        'Beach': 'Scenic',
        'Wildlife': 'Nature',
        'Wellness': 'Scenic',
        'Foodie': 'Food',
        'Romantic': 'Scenic',
        'Luxury': 'Architecture',
    }
    q = Q()
    for style in styles:
        cat = style_to_category.get(style)
        if cat:
            q |= Q(category=cat)

    if q:
        return HiddenGem.objects.filter(q).order_by('-rating')[:limit]

    return HiddenGem.objects.order_by('-rating')[:limit]
