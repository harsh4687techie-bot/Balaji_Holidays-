from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.trip_planner_view, name='trip_planner'),
    path('saved/', views.saved_trips_view, name='saved_trips'),
    path('<int:pk>/', views.trip_detail_view, name='trip_detail'),
    path('<int:pk>/itinerary/', views.itinerary_detail_view, name='itinerary_detail'),
    path('<int:pk>/save/', views.save_trip_view, name='save_trip'),
    path('<int:pk>/delete/', views.delete_trip_view, name='delete_trip'),
    path('share/<uuid:token>/', views.shared_trip_view, name='shared_trip'),
]
