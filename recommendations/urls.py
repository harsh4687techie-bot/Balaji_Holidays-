from django.urls import path
from . import views

urlpatterns = [
    path('', views.hidden_gems_view, name='hidden_gems'),
]
