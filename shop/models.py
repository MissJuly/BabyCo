from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from shop.choices import CATEGORY_CHOICES, LABEL_CHOICES, ADDRESS_CHOICES


class UserProfile(models.Model):
    """Stores the user profile"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username


class Item(models.Model):
    """This is a product being sold"""
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    label = models.CharField(choices=LABEL_CHOICES, max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self) -> str:
        return self.title


class OrderItem(models.Model):
    """This is an item added to cart"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    """This represents the shopping cart"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=True)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self) -> str:
        return self.user.username


class Address(models.Model):
    """user address for order fulfilment"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100, blank=True,
                           null=True, default='N/A')
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    """store payment data from user"""
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class Coupon(models.Model):
    """Stores all generated coupons"""
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self) -> str:
        return self.code


class Refund(models.Model):
    """Keeping track of refunds to orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self) -> str:
        return f'{self.pk}'
