import json
import random
from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import Http404
from .models import Trip, ItineraryItem, SavedTrip
from .forms import TripPlannerStep1Form, TripPlannerStep2Form


# ------------------------------------------------------------------
# Itinerary generation data: realistic activities per budget/style
# ------------------------------------------------------------------

ACTIVITIES_TEMPLATE = {
    'Morning': [
        {'title': 'Sunrise Exploration', 'description': 'Start the day with a serene sunrise walk through the old city quarters.', 'time_range': '07:00 AM - 09:00 AM'},
        {'title': 'Local Breakfast Tasting', 'description': 'Enjoy a curated spread of local morning delicacies at a beloved neighbourhood café.', 'time_range': '08:30 AM - 10:00 AM'},
        {'title': 'Heritage Site Tour', 'description': 'Guided visit to the most iconic cultural landmarks, with expert storytelling.', 'time_range': '09:00 AM - 11:30 AM'},
        {'title': 'Market Walk & Spice Tour', 'description': 'Wander through the vibrant morning market, sampling spices and street food.', 'time_range': '08:00 AM - 10:30 AM'},
    ],
    'Afternoon': [
        {'title': 'Lunch at a Rooftop Restaurant', 'description': 'Savour a relaxed, multi-course lunch with panoramic skyline views.', 'time_range': '01:00 PM - 02:30 PM'},
        {'title': 'Cultural Museum Visit', 'description': "Discover the region's rich history through curated exhibits and artefacts.", 'time_range': '02:00 PM - 04:30 PM'},
        {'title': 'Nature Hike & Viewpoint', 'description': 'A scenic 3-hour hike to a breathtaking viewpoint with photo opportunities.', 'time_range': '01:30 PM - 04:00 PM'},
        {'title': 'Spa & Wellness Session', 'description': 'Rejuvenating afternoon at a world-class spa featuring local treatment techniques.', 'time_range': '02:00 PM - 05:00 PM'},
    ],
    'Evening': [
        {'title': 'Sunset Cruise', 'description': 'Glide across the water on a private sunset cruise with canapés and cocktails.', 'time_range': '06:00 PM - 08:00 PM'},
        {'title': 'Fine Dining Experience', 'description': "A reservation at the destination's most celebrated restaurant for a gourmet evening meal.", 'time_range': '07:30 PM - 10:00 PM'},
        {'title': 'Night Market & Street Food Tour', 'description': 'Explore the buzzing night market, tasting local favourites under fairy lights.', 'time_range': '06:30 PM - 09:00 PM'},
        {'title': 'Live Cultural Performance', 'description': 'Attend a traditional dance or music show celebrating local heritage.', 'time_range': '07:00 PM - 09:30 PM'},
    ],
}

DAY_TITLES = [
    'Arrival & First Impressions',
    'Deep Dive into Culture',
    'Nature & Adventure Day',
    'Culinary Journey',
    'Hidden Gems & Local Life',
    'Relaxation & Reflection',
    'Exploration & Discovery',
    'Farewell & Memories',
]


def _serialize_form_data(form_data):
    """Convert QueryDict data into plain dict values that can be stored in the session."""
    serialized = {}
    for key, values in form_data.lists():
        serialized[key] = values[0] if len(values) == 1 else values
    return serialized


def generate_itinerary_items(trip):
    """Generate realistic ItineraryItem records for a trip."""
    ItineraryItem.objects.filter(trip=trip).delete()

    days = trip.duration_days or 5
    order = 0
    for day in range(1, days + 1):
        for tod, activities in [('MORNING', ACTIVITIES_TEMPLATE['Morning']),
                                 ('AFTERNOON', ACTIVITIES_TEMPLATE['Afternoon']),
                                 ('EVENING', ACTIVITIES_TEMPLATE['Evening'])]:
            activity = random.choice(activities)
            ItineraryItem.objects.create(
                trip=trip,
                day_number=day,
                time_of_day=tod,
                time_range=activity['time_range'],
                title=activity['title'],
                description=activity['description'],
                order=order,
            )
            order += 1


# ------------------------------------------------------------------
# Views
# ------------------------------------------------------------------

def trip_planner_view(request):
    """3-step trip planner wizard. Works for both guests and logged-in users."""
    step = int(request.GET.get('step', 1))
    step1_form = TripPlannerStep1Form(request.session.get('planner_step1'))
    step2_form = TripPlannerStep2Form(request.session.get('planner_step2'))

    if request.method == 'POST':
        current_step = int(request.POST.get('current_step', 1))

        if current_step == 1:
            step1_form = TripPlannerStep1Form(request.POST)
            if step1_form.is_valid():
                request.session['planner_step1'] = _serialize_form_data(request.POST)
                return redirect(f'{request.path}?step=2')

        elif current_step == 2:
            step2_form = TripPlannerStep2Form(request.POST)
            if step2_form.is_valid():
                request.session['planner_step2'] = _serialize_form_data(request.POST)
                return redirect(f'{request.path}?step=3')

        elif current_step == 3:
            # Final step — generate itinerary
            if not request.user.is_authenticated:
                messages.warning(request, 'Please sign in to save and view your personalized itinerary.')
                return redirect(f'/accounts/login/?next={request.path}?step=3')

            step1_data = request.session.get('planner_step1', {})
            step2_data = request.session.get('planner_step2', {})

            destination = step1_data.get('destination', 'Unknown Destination')
            start_date = step1_data.get('start_date') or None
            end_date = step1_data.get('end_date') or None
            traveler_count = int(step1_data.get('traveler_count', 2))
            budget = step2_data.get('budget', 'mid')
            styles = step2_data.get('travel_styles', [])
            if isinstance(styles, str):
                styles = [styles]
            elif not isinstance(styles, list):
                styles = [str(styles)]

            # Parse dates
            from datetime import date as date_cls
            import datetime as dt_mod
            parsed_start = None
            parsed_end = None
            if start_date:
                try:
                    parsed_start = dt_mod.date.fromisoformat(start_date)
                except ValueError:
                    pass
            if end_date:
                try:
                    parsed_end = dt_mod.date.fromisoformat(end_date)
                except ValueError:
                    pass

            trip = Trip.objects.create(
                user=request.user,
                title=f"{destination} Journey",
                destination_name=destination,
                start_date=parsed_start,
                end_date=parsed_end,
                traveler_count=traveler_count,
                budget=budget,
                travel_styles=json.dumps(styles),
            )
            generate_itinerary_items(trip)

            # Clear session
            request.session.pop('planner_step1', None)
            request.session.pop('planner_step2', None)

            return redirect('itinerary_detail', pk=trip.pk)

    # Summarise session data for step 3 review
    step1_data = request.session.get('planner_step1', {})
    step2_data = request.session.get('planner_step2', {})

    context = {
        'step': step,
        'step1_form': step1_form,
        'step2_form': step2_form,
        'summary_destination': step1_data.get('destination', ''),
        'summary_travelers': step1_data.get('traveler_count', '2'),
        'summary_budget': dict(Trip.BUDGET_CHOICES).get(step2_data.get('budget', 'mid'), 'Mid-range'),
        'summary_start': step1_data.get('start_date', ''),
        'summary_end': step1_data.get('end_date', ''),
    }
    return render(request, 'trips/planner.html', context)


@login_required
def itinerary_detail_view(request, pk):
    """Detailed itinerary view for a specific trip."""
    trip = get_object_or_404(Trip, pk=pk)

    # Allow owner or shared link access
    if trip.user != request.user:
        raise Http404

    items = trip.itinerary_items.order_by('day_number', 'order')

    # Group items by day
    days = {}
    for item in items:
        if item.day_number not in days:
            idx = item.day_number - 1
            days[item.day_number] = {
                'number': item.day_number,
                'title': DAY_TITLES[idx] if idx < len(DAY_TITLES) else f'Day {item.day_number}',
                'items': {'MORNING': [], 'AFTERNOON': [], 'EVENING': []},
            }
        days[item.day_number]['items'][item.time_of_day].append(item)

    is_saved = SavedTrip.objects.filter(user=request.user, trip=trip).exists()

    context = {
        'trip': trip,
        'days': days,
        'is_saved': is_saved,
    }
    return render(request, 'trips/itinerary.html', context)


def shared_trip_view(request, token):
    """Public shared trip view using UUID share_token — no auth required."""
    trip = get_object_or_404(Trip, share_token=token)
    items = trip.itinerary_items.order_by('day_number', 'order')

    days = {}
    for item in items:
        if item.day_number not in days:
            idx = item.day_number - 1
            days[item.day_number] = {
                'number': item.day_number,
                'title': DAY_TITLES[idx] if idx < len(DAY_TITLES) else f'Day {item.day_number}',
                'items': {'MORNING': [], 'AFTERNOON': [], 'EVENING': []},
            }
        days[item.day_number]['items'][item.time_of_day].append(item)

    context = {
        'trip': trip,
        'days': days,
        'is_shared_view': True,
        'is_saved': False,
    }
    return render(request, 'trips/itinerary.html', context)


@login_required
def saved_trips_view(request):
    """View all saved trips for the current user."""
    trips = Trip.objects.filter(user=request.user).prefetch_related('itinerary_items')
    saved = SavedTrip.objects.filter(user=request.user).select_related('trip')

    context = {
        'trips': trips,
        'saved_trips': saved,
    }
    return render(request, 'trips/saved_trips.html', context)


@login_required
def trip_detail_view(request, pk):
    """Trip detail summary view."""
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    items = trip.itinerary_items.order_by('day_number', 'order')
    is_saved = SavedTrip.objects.filter(user=request.user, trip=trip).exists()

    context = {
        'trip': trip,
        'items': items,
        'is_saved': is_saved,
    }
    return render(request, 'trips/detail.html', context)


@login_required
@require_POST
def save_trip_view(request, pk):
    """Toggle saving/unsaving a trip."""
    trip = get_object_or_404(Trip, pk=pk)
    saved, created = SavedTrip.objects.get_or_create(user=request.user, trip=trip)
    if not created:
        saved.delete()
        messages.info(request, f'"{trip.title}" removed from saved trips.')
    else:
        messages.success(request, f'"{trip.title}" added to your saved trips!')
    return redirect(request.META.get('HTTP_REFERER', 'saved_trips'))


@login_required
@require_POST
def delete_trip_view(request, pk):
    """Delete a trip created by the current user."""
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    title = trip.title
    trip.delete()
    messages.success(request, f'Trip "{title}" has been deleted.')
    return redirect('saved_trips')
