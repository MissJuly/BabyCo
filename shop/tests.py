from django.test import TestCase
from .models import Item

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
            f"/product/{self.item.slug}/",
        )

    def test_get_add_to_cart_url(self):
        self.assertEqual(
            self.item.get_add_to_cart_url(),
            f"/add-to-cart/{self.item.slug}/",
        )

    def test_get_remove_from_cart_url(self):
        self.assertEqual(
            self.item.get_remove_from_cart_url(),
            f"/remove-from-cart/{self.item.slug}/",
        )
