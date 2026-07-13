from django.conf import settings

def maps_key_processor(request):
    """
    Makes the Maps API Key available to all templates for Google Maps integration.
    """
    return {
        'MAPS_API_KEY': getattr(settings, 'MAPS_API_KEY', '')
    }
