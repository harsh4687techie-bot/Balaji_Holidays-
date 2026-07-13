from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, SignUpForm, ProfileUpdateForm, PreferencesForm
from .models import UserProfile, UserPreference
from trips.models import Trip, SavedTrip


def login_signup_view(request):
    """Combined login/signup page matching the Stitch design."""
    login_form = LoginForm()
    signup_form = SignUpForm()
    active_tab = request.GET.get('tab', 'signin')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'signin':
            active_tab = 'signin'
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password. Please try again.')

        elif action == 'signup':
            active_tab = 'signup'
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, f'Welcome to Balaji Holidays, {user.first_name}! Your journey begins now.')
                return redirect('home')
            else:
                messages.error(request, 'Please fix the errors below.')

    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'active_tab': active_tab,
    }
    return render(request, 'accounts/login_signup.html', context)


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out. See you soon!')
    return redirect('landing')


@login_required
def profile_view(request):
    """Profile and settings page."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    preferences, _ = UserPreference.objects.get_or_create(user=request.user)

    profile_form = ProfileUpdateForm(instance=profile)
    prefs_form = PreferencesForm(instance=preferences)
    active_tab = request.GET.get('tab', 'interests')

    if request.method == 'POST':
        tab = request.POST.get('tab', 'interests')
        active_tab = tab

        if tab == 'account':
            profile_form = ProfileUpdateForm(request.POST, instance=profile)
            if profile_form.is_valid():
                pf = profile_form.save(commit=False)
                pf.save()
                # Update first_name/last_name on auth User
                request.user.first_name = profile_form.cleaned_data.get('first_name', request.user.first_name)
                request.user.last_name = profile_form.cleaned_data.get('last_name', request.user.last_name)
                request.user.save()
                messages.success(request, 'Account details updated successfully.')
                return redirect(f'{request.path}?tab=account')

        elif tab in ['interests', 'preferences', 'notifications']:
            prefs_form = PreferencesForm(request.POST, instance=preferences)
            if prefs_form.is_valid():
                prefs_form.save()
                messages.success(request, 'Your preferences have been saved.')
                return redirect(f'{request.path}?tab={tab}')

    # Fetch user trip stats
    trips_count = Trip.objects.filter(user=request.user).count()
    saved_count = SavedTrip.objects.filter(user=request.user).count()

    context = {
        'profile': profile,
        'preferences': preferences,
        'profile_form': profile_form,
        'prefs_form': prefs_form,
        'active_tab': active_tab,
        'trips_count': trips_count,
        'saved_count': saved_count,
    }
    return render(request, 'accounts/profile.html', context)
