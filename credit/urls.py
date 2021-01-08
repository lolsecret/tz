from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.IinView.as_view(), name='api'),
]