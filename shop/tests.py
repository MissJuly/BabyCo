from django.contrib.auth.models import User
from django.test import TestCase
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from shop.forms import CheckoutForm, CouponForm, RefundForm, PaymentForm


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            title="Test Product",
            price=100.0,
            discount_price=80.0,
            category="Test Category",
            label="Test Label",
            slug="test-product",
            image="bicycle.jpg",
            description="This is a test product description.",
        )

    def test_item_str(self):
        self.assertEqual(str(self.item), "Test Product")

    def test_get_absolute_url(self):
        url = reverse("shop:product", kwargs={"slug": self.item.slug})
        self.assertEqual(self.item.get_absolute_url(), url)

    def test_get_add_to_cart_url(self):
        url = reverse("shop:add-to-cart", kwargs={"slug": self.item.slug})
        self.assertEqual(self.item.get_add_to_cart_url(), url)

    def test_get_remove_from_cart_url(self):
        url = reverse("shop:remove-from-cart", kwargs={"slug": self.item.slug})
        self.assertEqual(self.item.get_remove_from_cart_url(), url)

    def test_image_resizing(self):
        # Create a sample image
        img = Image.new("RGB", (400, 400))
        img.save("dino.jpg")

        # Create an item with the sample image
        item_with_image = Item.objects.create(
            title="Test Product with Image",
            price=100.0,
            category="Test Category",
            label="Test Label",
            slug="test-product-with-image",
            image="dino.jpg",
            description="This is a test product description with an image.",
        )
        item_with_image.image = "dino.jpg"
        item_with_image.save()

        # Check if the image is resized to 300x300
        img = Image.open(item_with_image.image.path)
        self.assertLessEqual(img.width, 300)
        self.assertLessEqual(img.height, 300)

    def tearDown(self):
        # Clean up by removing the sample image file
        try:
            import os
            os.remove("bicycle.jpg")
        except FileNotFoundError:
            pass


class OrderModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.order = Order.objects.create(
            user=self.user,
            ref_code="TEST123",
            ordered_date=timezone.now(),
            ordered=False,
        )
        self.item = Item.objects.create(
            title="Test Item",
            price=10.0,
            category="TestCategory",
            label="TestLabel",
            slug="test-item",
            description="This is a test item description.",
            image="bicycle.jpg",
        )
        self.order_item = OrderItem.objects.create(
            user=self.user,
            ordered=False,
            item=self.item,
            quantity=2,
        )
        self.order.items.add(self.order_item)

    def test_order_str(self):
        self.assertEqual(str(self.order), self.user.username)

    def test_get_total(self):
        self.assertEqual(self.order.get_total(), 20.0)


class OrderItemModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.item = Item.objects.create(
            title="Test Item",
            price=10.0,
            category="TestCategory",
            label="TestLabel",
            slug="test-item",
            description="This is a test item description.",
            image="bicycle.jpg",
        )
        self.order_item = OrderItem.objects.create(
            user=self.user,
            ordered=False,
            item=self.item,
            quantity=2,
        )

    def test_order_item_str(self):
        self.assertEqual(
            str(self.order_item),
            "2 of Test Item",
        )

    def test_get_total_item_price(self):
        self.assertEqual(self.order_item.get_total_item_price(), 20.0)

    def test_get_total_discount_item_price(self):
        self.item.discount_price = 8.0
        self.assertEqual(self.order_item.get_total_discount_item_price(), 16.0)

    def test_get_amount_saved(self):
        self.item.discount_price = 8.0
        self.assertEqual(self.order_item.get_amount_saved(), 4.0)

    def test_get_final_price(self):
        self.item.discount_price = 8.0
        self.assertEqual(self.order_item.get_final_price(), 16.0)


class ShopFormsTest(TestCase):
    def test_checkout_form_valid(self):
        data = {
            'shipping_address': '123 Street',
            'shipping_address2': 'Apt 456',
            'shipping_country': 'US',
            'shipping_zip': '12345',
            'billing_address': '789 Avenue',
            'billing_address2': 'Suite 101',
            'billing_country': 'CA',
            'billing_zip': 'V6B 2W9',
            'same_billing_address': True,
            'set_default_shipping': True,
            'use_default_shipping': True,
            'set_default_billing': True,
            'use_default_billing': True,
            'payment_option': 'S',
        }
        form = CheckoutForm(data)
        assert form.is_valid()

    def test_coupon_form_valid(self):
        data = {
            'code': 'TESTCODE123',
        }
        form = CouponForm(data)
        assert form.is_valid()

    def test_refund_form_valid(self):
        data = {
            'ref_code': 'REF123',
            'message': 'This is a test refund request.',
            'email': 'test@example.com',
        }
        form = RefundForm(data)
        assert form.is_valid()

    def test_payment_form_valid(self):
        data = {
            'stripeToken': 'tok_visa',
            'save': True,
            'use_default': True,
        }
        form = PaymentForm(data)
        assert form.is_valid()
