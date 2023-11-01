from typing import Any
from django.db.models.query import QuerySet
from users.models import UserProfile
from shop.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import json


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        # get user profile
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)

        # get order history
        orders = Order.objects.filter(user=user)
        orders_complete = []
        orders_open = []
        for order in orders:
            if order.ordered == True:
                orders_complete.append(order)
            else:
                orders_open.append(order)

        context.update({
            'profile': profile,
            'orders': orders,
            'orders_complete': orders_complete,
            'orders_open': orders_open
        })
        return context

    def post(self, request, *args, **kwargs):
        """"""
        def is_ajax(request):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        message = None
        if is_ajax(request=request):
            user = request.user
            username = request.POST.get("username")
            if user.username == username:
                user.is_active = False
                user.save()
                msg = 'Profile disabled successfully'
                data = json.dumps({
                    'msg': msg,
                })
                return JsonResponse({'data': data}, status=200)
            else:
                msg = "Username mismatch. Please try again!"
                data = json.dumps({
                    'msg': msg,
                })
                return JsonResponse({'data': data}, status=404)
        else:
            pass
        return render(request, "users/settings.html", {'message': message})


class OrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the total amount and pass it to the context
        total_amount = 0
        for order_item in context['order'].items.all():
            total_amount += order_item.get_total_item_price()

        context['total_amount'] = total_amount
        return context
