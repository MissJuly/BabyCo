from django.shortcuts import render
from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'landing-page.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'

class TermsConditionView(TemplateView):
    template_name = 'terms-condition.html'
