from django.urls import path
from users.views import SettingsView
from . import views


urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
    path('order/<int:pk>/', views.OrderDetailsView.as_view(), name='order_details'),
]
