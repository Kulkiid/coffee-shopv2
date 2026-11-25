from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import MENU_ITEMS, LoginForm, OrderForm


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")

    return render(request, "Login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def home_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order_name = form.cleaned_data["name"]
            order_email = form.cleaned_data["email"]
            order_location = form.cleaned_data["location"]
            order_codes = form.cleaned_data["coffee"]
            menu_items = {code: (label, price) for code, label, price in MENU_ITEMS}
            selected_items = [menu_items[code] for code in order_codes]
            order_total = sum(
                (price for _label, price in selected_items), Decimal("0.00")
            )
            return render(
                request,
                "Receipt.html",
                {
                    "order_reference": uuid4().hex[:10].upper(),
                    "order_date": timezone.localtime(),
                    "customer": {
                        "name": order_name,
                        "email": order_email,
                        "location": order_location,
                    },
                    "receipt_items": [
                        {"name": label, "price": price}
                        for label, price in selected_items
                    ],
                    "order_total": order_total,
                },
            )
    else:
        form = OrderForm()

    return render(request, "Coffee.html", {"form": form})
