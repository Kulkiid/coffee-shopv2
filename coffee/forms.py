from decimal import Decimal

from django import forms
from django.contrib.auth.forms import AuthenticationForm


MENU_ITEMS = (
    ("hot_beverages", "Hot Beverages", Decimal("2.50")),
    ("cold_beverages", "Cold Beverages", Decimal("3.50")),
    ("refreshments", "Refreshments", Decimal("2.75")),
    ("special_combo", "Special Combo", Decimal("7.00")),
    ("desserts", "Desserts", Decimal("4.00")),
    ("burger_and_fries", "Burger and French Fries", Decimal("8.00")),
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your name", "autocomplete": "username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )


class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Your Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your name", "autocomplete": "name"}
        ),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "you@example.com", "autocomplete": "email"}
        ),
    )
    location = forms.CharField(
        max_length=200,
        label="Your Location",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Street, city, or pickup location",
                "autocomplete": "street-address",
            }
        ),
    )
    coffee = forms.MultipleChoiceField(
        label="Choose from the menu",
        widget=forms.CheckboxSelectMultiple,
        choices=[
            (value, f"{label} - From ${price:.2f}")
            for value, label, price in MENU_ITEMS
        ],
    )
