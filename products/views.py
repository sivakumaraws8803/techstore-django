from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related("category")
    selected = request.GET.get("category")
    if selected:
        products = products.filter(category__slug=selected)
    return render(request, "products/home.html", {
        "categories": categories,
        "products": products,
        "selected_category": selected,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/detail.html", {"product": product})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = request.session.get("cart", {})
    key = str(product.id)
    quantity = int(cart.get(key, 0))
    if product.stock > quantity:
        cart[key] = quantity + 1
        request.session["cart"] = cart
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id), is_active=True)
        except (Product.DoesNotExist, ValueError):
            continue
        line_total = product.price * quantity
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
    return render(request, "products/cart.html", {"items": items, "total": total})


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")
