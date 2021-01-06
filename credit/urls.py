from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.IinView.as_view(), name='api'),
    path('app/', views.ApplicationView.as_view(), name='app_view'),
    path('borrower', views.BorrowerView.as_view())
]