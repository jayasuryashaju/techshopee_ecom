# from account.models import user
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from products.models import Category, Product, Banner

from cart.models import Cart, Wishlist


# Create your views here.


def home(request):
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    categories = Category.objects.all()
    products = Product.objects.all()
    category_id = request.GET.get('category')
    banners = Banner.objects.all()
    for banner in banners:
        print(banner.product.name)
    if category_id:
        products = products.filter(category_id=category_id)

    if email or phone_number:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_count = cart_items.count()
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_count = wishlist.count()

        user = request.user
        context = {
            'user': user,
            'products': products,
            'categories': categories,
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_count': cart_count,
            'wishlist_count': wishlist_count,
            'banners': banners

        }
    else:
        context = {
            'products': products,
            'categories': categories,
            'banners': banners
        }

    return render(request, 'index.html', context)


def search(request):
    category = Category.objects.all()
    if 'search' in request.GET:
        keyword = request.GET['search']
        if keyword:
            products = Product.objects.order_by('id').filter(name__icontains=keyword)
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'products': paged_products,
        'category': category
    }
    return render(request, 'category_list.html', context)
