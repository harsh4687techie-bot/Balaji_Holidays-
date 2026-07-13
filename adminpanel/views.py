from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from destinations.models import Destination
from recommendations.models import HiddenGem
from trips.models import Trip
from core.models import FAQ
import json


def staff_required(view_func):
    """Decorator that redirects non-staff users to login."""
    decorated = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/accounts/login/?next=/adminpanel/',
    )(view_func)
    return decorated


@staff_required
def admin_dashboard_view(request):
    """Admin dashboard showing key metrics."""
    context = {
        'total_users': User.objects.count(),
        'total_destinations': Destination.objects.count(),
        'total_trips': Trip.objects.count(),
        'total_gems': HiddenGem.objects.count(),
        'total_faqs': FAQ.objects.count(),
        'featured_destinations': Destination.objects.filter(is_featured=True).count(),
        'recent_users': User.objects.order_by('-date_joined')[:10],
        'recent_trips': Trip.objects.select_related('user').order_by('-created_at')[:10],
        'destinations': Destination.objects.all()[:20],
    }
    return render(request, 'adminpanel/dashboard.html', context)


@staff_required
def manage_destinations_view(request):
    """Admin: list, add, or delete destinations."""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            categories = request.POST.getlist('categories')
            Destination.objects.create(
                name=request.POST.get('name', ''),
                country=request.POST.get('country', ''),
                description=request.POST.get('description', ''),
                short_description=request.POST.get('short_description', ''),
                price_per_person=request.POST.get('price_per_person', 0) or 0,
                rating=request.POST.get('rating', 4.5) or 4.5,
                categories=json.dumps(categories),
                image_url=request.POST.get('image_url', ''),
                latitude=request.POST.get('latitude', 0) or 0,
                longitude=request.POST.get('longitude', 0) or 0,
                is_featured='is_featured' in request.POST,
                is_popular='is_popular' in request.POST,
                best_season=request.POST.get('best_season', 'Year-round'),
                language=request.POST.get('language', ''),
                currency=request.POST.get('currency', ''),
            )
            messages.success(request, 'Destination added successfully.')

        elif action == 'delete':
            dest_id = request.POST.get('destination_id')
            dest = get_object_or_404(Destination, pk=dest_id)
            dest.delete()
            messages.success(request, f'Destination "{dest.name}" deleted.')

        return redirect('admin_destinations')

    destinations = Destination.objects.all()
    context = {
        'destinations': destinations,
        'category_choices': Destination.CATEGORY_CHOICES,
    }
    return render(request, 'adminpanel/manage_destinations.html', context)


@staff_required
def manage_faqs_view(request):
    """Admin: list, add, or delete FAQ entries."""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            FAQ.objects.create(
                question=request.POST.get('question', ''),
                answer=request.POST.get('answer', ''),
                category=request.POST.get('category', 'General'),
            )
            messages.success(request, 'FAQ entry added successfully.')

        elif action == 'delete':
            faq_id = request.POST.get('faq_id')
            faq = get_object_or_404(FAQ, pk=faq_id)
            faq.delete()
            messages.success(request, 'FAQ entry deleted.')

        return redirect('admin_faqs')

    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
        'categories': FAQ.CATEGORY_CHOICES,
    }
    return render(request, 'adminpanel/manage_faqs.html', context)


@staff_required
def manage_gems_view(request):
    """Admin: list, add, or delete Hidden Gems."""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            dest_id = request.POST.get('destination')
            destination = Destination.objects.filter(pk=dest_id).first() if dest_id else None
            HiddenGem.objects.create(
                destination=destination,
                name=request.POST.get('name', ''),
                description=request.POST.get('description', ''),
                rating=request.POST.get('rating', 4.5) or 4.5,
                image_url=request.POST.get('image_url', ''),
                latitude=request.POST.get('latitude', 0) or 0,
                longitude=request.POST.get('longitude', 0) or 0,
                why_special=request.POST.get('why_special', ''),
                transport_info=request.POST.get('transport_info', ''),
                category=request.POST.get('category', 'Nature'),
                location_label=request.POST.get('location_label', ''),
            )
            messages.success(request, 'Hidden Gem added successfully.')

        elif action == 'delete':
            gem_id = request.POST.get('gem_id')
            gem = get_object_or_404(HiddenGem, pk=gem_id)
            gem.delete()
            messages.success(request, f'Hidden Gem "{gem.name}" deleted.')

        return redirect('admin_gems')

    gems = HiddenGem.objects.select_related('destination').all()
    destinations = Destination.objects.all()
    context = {
        'gems': gems,
        'destinations': destinations,
        'category_choices': HiddenGem.CATEGORY_CHOICES,
    }
    return render(request, 'adminpanel/manage_gems.html', context)
