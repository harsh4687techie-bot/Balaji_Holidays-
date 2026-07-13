from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard_view, name='admin_dashboard'),
    path('destinations/', views.manage_destinations_view, name='admin_destinations'),
    path('gems/', views.manage_gems_view, name='admin_gems'),
    path('faqs/', views.manage_faqs_view, name='admin_faqs'),
]
