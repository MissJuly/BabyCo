from django.contrib.auth.models import User
from django.test import TestCase
from .models import Item, Order, OrderItem
from django.utils import timezone


class ItemModelTest(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            title="Test Item",
            price=10.0,
            category="TestCategory",
            label="TestLabel",
            slug="test-item",
            description="This is a test item description.",
        )

    def test_item_str(self):
        self.assertEqual(str(self.item), "Test Item")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.item.get_absolute_url(),
            f"/shop/product/{self.item.slug}/",
        )

    def test_get_add_to_cart_url(self):
        self.assertEqual(
            self.item.get_add_to_cart_url(),
            f"/shop/add-to-cart/{self.item.slug}/",
        )

    def test_get_remove_from_cart_url(self):
        self.assertEqual(
            self.item.get_remove_from_cart_url(),
            f"/shop/remove-from-cart/{self.item.slug}/",
        )


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
