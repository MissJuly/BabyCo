from django.urls import path
from users.views import SettingsView

urlpatterns = [
    path('settings/', SettingsView.as_view(), name='settings'),
]
