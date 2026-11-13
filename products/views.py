from decimal import Decimal, InvalidOperation

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import SharedProduct


def home(request):
    selected_category = request.GET.get("category", "").strip()

    products = SharedProduct.objects.using("shared_products").filter(
        is_active=True
    )

    if selected_category:
        products = products.filter(category=selected_category)

    categories = (
        SharedProduct.objects.using("shared_products")
        .filter(is_active=True)
        .exclude(category__isnull=True)
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    return render(request, "products/home.html", {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
    })


def product_detail(request, product_id):
    product = get_object_or_404(
        SharedProduct.objects.using("shared_products"),
        pk=product_id,
        is_active=True,
    )
    return render(request, "products/detail.html", {"product": product})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(
        SharedProduct.objects.using("shared_products"),
        pk=product_id,
        is_active=True,
    )

    cart = request.session.get("cart", {})
    key = str(product.id)

    try:
        quantity = int(cart.get(key, 0))
    except (TypeError, ValueError):
        quantity = 0

    if quantity < 0:
        quantity = 0

    if product.stock > quantity:
        cart[key] = quantity + 1
        request.session["cart"] = cart

    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")
    valid_cart = {}

    for product_id, quantity in cart.items():
        try:
            product_id = int(product_id)
            quantity = int(quantity)
            if quantity <= 0:
                continue

            product = SharedProduct.objects.using(
                "shared_products"
            ).get(pk=product_id, is_active=True)

            quantity = min(quantity, product.stock)
            if quantity <= 0:
                continue

            line_total = product.price * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            })
            total += line_total
            valid_cart[str(product.id)] = quantity

        except (SharedProduct.DoesNotExist, TypeError, ValueError, InvalidOperation):
            continue

    request.session["cart"] = valid_cart

    return render(request, "products/cart.html", {
        "items": items,
        "total": total,
    })


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")
