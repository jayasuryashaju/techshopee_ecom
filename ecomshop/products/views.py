from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.models import Cart


# Create your views here.


def product_list(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.filter(category_id=category_id)
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    cart_items = []
    total_price = 0
    cart_count = 0
    if email or phone_number:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_count = cart_items.count()

    # Pagination
    paginator = Paginator(products, 5)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)

    # Counters
    total_products = Product.objects.filter(category_id=category_id).count()
    num_products_shown = len(products)

    context = {
        'categories': categories,
        'products': products,
        'total_products': total_products,
        'num_products_shown': num_products_shown,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    }
    return render(request, 'category_list.html', context)


def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    cart_items = []
    total_price = 0
    cart_count = 0

    if email or phone_number:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_count = cart_items.count()
    context = {'product': product,
               'total_price': total_price,
               'cart_count': cart_count,
               'cart_items': cart_items,
               }
    return render(request, 'product_view.html', context)
