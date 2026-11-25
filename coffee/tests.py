from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import OrderForm


class OrderFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Blessing", password="12345"
        )
        self.client.force_login(self.user)

    def test_order_choices_match_the_website_menu(self):
        choice_values = [
            value for value, _label in OrderForm.base_fields["coffee"].choices
        ]

        self.assertEqual(
            choice_values,
            [
                "hot_beverages",
                "cold_beverages",
                "refreshments",
                "special_combo",
                "desserts",
                "burger_and_fries",
            ],
        )
        self.assertNotIn("cappuccino", choice_values)
        self.assertIsInstance(
            OrderForm.base_fields["coffee"].widget, forms.CheckboxSelectMultiple
        )

    def test_valid_menu_order_returns_confirmation(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Jordan",
                "email": "jordan@example.com",
                "location": "Main Street",
                "coffee": ["hot_beverages", "desserts"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Receipt.html")
        self.assertContains(response, "Thanks, Jordan.")
        self.assertContains(response, "Hot Beverages")
        self.assertContains(response, "Desserts")
        self.assertContains(response, "$2.50")
        self.assertContains(response, "$4.00")
        self.assertContains(response, "$6.50")
        self.assertContains(response, "jordan@example.com")
        self.assertContains(response, "Main Street")
        self.assertContains(response, "Print Receipt")

    def test_cappuccino_is_not_a_valid_order_choice(self):
        form = OrderForm(
            data={
                "name": "Jordan",
                "email": "jordan@example.com",
                "location": "Main Street",
                "coffee": ["cappuccino"],
            }
        )

        self.assertFalse(form.is_valid())

    def test_order_page_renders_an_image_for_each_menu_choice(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="order-menu-option"', count=6)
        for image_name in [
            "hot-beverages.png",
            "cold-beverages.png",
            "refreshment.png",
            "special-combo.png",
            "desserts.png",
            "burger-frenchfries.png",
        ]:
            with self.subTest(image=image_name):
                self.assertContains(response, image_name)

    def test_order_summary_and_total_controls_render(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "My Orders")
        self.assertContains(response, 'id="selected-order-list"')
        self.assertContains(response, 'id="order-total-amount"')

    def test_receipt_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("home"))

        self.assertRedirects(response, f"{reverse('login')}?next=/home/")

    def test_root_always_renders_login_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Login.html")

    def test_login_page_authenticates_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("login"), {"username": "Blessing", "password": "12345"}
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
