from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from shop.models import Item

class LandingPageView(ListView):
    template_name = 'landing-page.html'
    model = Item
    context_object_name = "items"
    paginate_by = 8
    ordering = ['-pk']


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy-policy.html'


class TermsConditionView(TemplateView):
    template_name = 'terms-condition.html'
