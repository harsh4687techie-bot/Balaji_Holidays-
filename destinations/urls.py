from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_search_view, name='destination_search'),
    path('map/', views.map_view, name='map_view'),
    path('<int:pk>/', views.destination_detail_view, name='destination_detail'),
]
