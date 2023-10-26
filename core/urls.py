from django.urls import path
from .views import LandingPageView, PrivacyPolicyView, TermsConditionView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('privacypolicy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('termsandcondition/', PrivacyPolicyView.as_view(), name='terms'),
]
