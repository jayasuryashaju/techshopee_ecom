from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from .forms import OrderForm
from .models import Cart, Wishlist, Order, Coupon, OrderItem
from products.models import Product
from user_profile.models import UserAddress
import razorpay


# Create your views here.


def custom_404(request, exception):
    return render(request, '404.html', context={})


@login_required(login_url='account:user_signin')
def add_to_cart(request, product_id):
    print('adding item to cart')
    product = get_object_or_404(Product, id=product_id)
    if 'quantity' in request.POST:
        selected_quantity = int(request.POST['quantity'])
    else:
        selected_quantity = 1

    cart = Cart.objects.filter(user=request.user, product=product).first()

    if cart:
        # cart object already exists for this user and product, update quantity
        cart.quantity += selected_quantity
        cart.save()
    else:
        # create a new cart object with the selected quantity
        cart = Cart(user=request.user, product=product, quantity=selected_quantity)
        cart.save()
    # messages.success(request, f"{selected_quantity} {product.name}(s) added to your cart.")
    return redirect('cart:cart_detail')


@csrf_exempt
def check_stock(request):
    print('hei1')
    product_id = request.POST['product_id']
    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity != 0:
        print('hei')
        return JsonResponse({'in_stock': True})
    else:
        return JsonResponse({'in_stock': False})


# @login_required(login_url='account:user_signin')
# @csrf_exempt
# def update_cart_item(request):
#     cartItemId = request.POST.get('cart_item_id')
#     quantity = request.POST.get('quantity')
#     product = get_object_or_404(Product, id=cartItemId)
#     cart_items = Cart.objects.filter(user=request.user)
#     cart_item = Cart.objects.filter(user=request.user, product=product).first()
#     cart_item.quantity = quantity
#     cart_item.save()
#     total_price = 0
#     if 'total_cost' in request.session:
#         request.session.pop('total_cost', None)
#         request.session.modified = True
#     for items in cart_items:
#         total_price += items.get_total_cost()
#     return JsonResponse({'total_price': total_price})

@login_required(login_url='account:user_signin')
@csrf_exempt
def update_cart_item(request):
    cart_item_id = request.POST.get('cart_item_id')
    quantity = request.POST.get('quantity')
    product = get_object_or_404(Product, id=cart_item_id)
    cart_items = Cart.objects.filter(user=request.user)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if product.selling_price != 0:
        cart_item_price = product.selling_price
    else:
        cart_item_price = product.price
    cart_item.quantity = quantity
    cart_item.price = cart_item_price
    cart_item.save()
    total_price = 0
    if 'total_cost' in request.session:
        request.session.pop('total_cost', None)
        request.session.modified = True
    for item in cart_items:
        total_price += item.get_total_cost()
    return JsonResponse({'total_price': total_price})


@login_required(login_url='account:user_signin')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if 'total_cost' in request.session:
        request.session.pop('total_cost', None)
        request.session.modified = True
    # product_name = cart_item.product.name
    cart_item.delete()
    # messages.success(request, f"{product_name} removed from your cart."
    return redirect('cart:cart_detail')


# @login_required(login_url='account:user_signin')
# def cart_detail(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_cost = 0
#     for cart_item in cart_items:
#         total_cost += cart_item.get_total_cost()
#
#     print(total_cost, "this is the cart total price")
#     cart_count = cart_items.count()
#     return render(request, 'cart.html',
#                   {'cart_items': cart_items, 'total_price': total_cost, 'cart_count': cart_count})

@login_required(login_url='account:user_signin')
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    request.session.pop('coupon', None)
    request.session.pop('total_cost', None)
    request.session.modified = True
    total_cost = 0
    for cart_item in cart_items:
        if cart_item.product.selling_price != 0:
            cart_item.price = cart_item.product.selling_price
        else:
            cart_item.price = cart_item.product.price
        total_cost += cart_item.get_total_cost()

    print(total_cost, "this is the cart total price")
    cart_count = cart_items.count()
    return render(request, 'cart.html',
                  {'cart_items': cart_items, 'total_price': total_cost, 'cart_count': cart_count})


@login_required(login_url='account:user_signin')
def wishlist_detail(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_count = wishlist.count()
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'wishlist_count': wishlist_count})


@login_required(login_url='account:user_signin')
@csrf_exempt
def add_to_wishlist(request, product_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            # Product is already in the wishlist
            return JsonResponse({'status': 'error', 'message': 'Product is already in your wishlist.'})
        else:
            # Add product to the wishlist
            wishlist.save()
            return JsonResponse({'status': 'success', 'message': 'Product added to your wishlist.'})


@login_required(login_url='account:user_signin')
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    # product_name = cart_item.product.name
    wishlist_item.delete()
    # messages.success(request, f"{product_name} removed from your cart."
    return redirect('cart:wishlist_detail')


def proceed_to_pay(request):
    global shipping_cost, discount
    total_price = 0
    discount = 0.00
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.get_total_cost() for item in cart_items)
    if 'total_cost' in request.session:
        total_price = request.session['total_cost']
    if request.GET.get('shipping_options'):
        shipping_options = request.GET.get('shipping_options')
        if shipping_options == 'free_shipping':
            shipping_cost = 0.00
        elif shipping_options == 'faster_shipping':
            shipping_cost = 100.00
        if 'total_cost' in request.session:
            total_price = request.session['total_cost']
            total_price = float(total_price) + float(shipping_cost)
            print('total cost', total_price)
        else:
            total_price = float(total_price) + float(shipping_cost)
            print(total_price, 'i am 2nd total cost')
    if 'coupon' in request.session:
        coupon = request.session['coupon']
        coupon = get_object_or_404(Coupon, code=coupon, active=True, valid_from__lte=timezone.now(),
                                   valid_to__gte=timezone.now())
        discount = coupon.discount_value
        print(discount, 'i am the discount proceed to pay')
    total_price = round(total_price)
    print("total from proceed to pay", total_price)
    return JsonResponse({

        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'discount': discount,
    })


def checkout(request):
    global shipping_cost
    discount = 0.00
    addresses = UserAddress.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    if 'total_cost' in request.session:
        total_cost = request.session['total_cost']
    else:
        total_cost = sum(item.get_total_cost() for item in cart_items)

    if 'coupon' in request.session:
        coupon = request.session['coupon']
        coupon = get_object_or_404(Coupon, code=coupon, active=True, valid_from__lte=timezone.now(),
                                   valid_to__gte=timezone.now())
        discount = coupon.discount_value

    coupons = Coupon.objects.all()
    active_coupon = request.session.get('coupon')
    print(active_coupon, 'i am the active coupon')
    user = request.user
    form = OrderForm()
    if request.method == 'POST':
        shipping_options = request.POST.get('shipping_options')
        shipping_address_id = request.POST['address']
        if shipping_options == 'free_shipping':
            shipping_cost = 0.00
        elif shipping_options == 'faster_shipping':
            shipping_cost = 100.00
        if 'total_cost' in request.session:
            total_cost = request.session['total_cost']
            total_cost = float(total_cost) + float(shipping_cost)
            print('total cost', total_cost)
        else:
            total_cost = float(total_cost) + float(shipping_cost)
            print(total_cost, 'i am 2nd total cost')

        payment_method = request.POST['payment_option']
        shipping_address = UserAddress.objects.get(id=shipping_address_id)
        if payment_method == 'razorpay':
            print('hello i am razorpay')
            # Create a new order object but do not save it yet
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                status=Order.PENDING,
                total_price=total_cost
            )
            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_item.save()
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()
            cart_items.delete()

            # Initialize Razorpay client with your account's API key and secret
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Create a Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(total_cost * 100),  # Razorpay amount is in paisa
                'currency': 'INR',
                'payment_capture': '1',  # Auto capture payment
            })

            # Save Razorpay order ID to your order object
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            request.session.pop('coupon', None)
            request.session.pop('total_cost', None)
            request.session.modified = True

            # Return Razorpay order ID to the frontend
            return JsonResponse({'razorpay_order_id': razorpay_order['id']})
        else:
            print('hello i am cash on delivery')
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                status=Order.PENDING,
                total_price=total_cost
            )
            for cart_item in cart_items:
                print("hei i am proic", cart_item.product.price)
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_item.save()
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()
            cart_items.delete()
            order.save()
            request.session.pop('coupon', None)
            request.session.pop('total_cost', None)
            request.session.modified = True

            return redirect('cart:order_list')

    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'user': user,
        'form': form,
        'coupon': coupons,
        'active_coupon': active_coupon,
        'discount': discount

    }

    return render(request, 'checkout.html', context)


@login_required(login_url='account:user_signin')
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders
    }

    return render(request, 'dashboard_orders.html', context)


@login_required(login_url='account:user_signin')
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    print(order.id, 'hellow i am order id')
    orders = OrderItem.objects.filter(order_id=order_id)
    context = {
        'orders': orders,
        'order': order,
    }
    return render(request, 'dashboard_order_details.html', context)


@login_required(login_url='account:user_signin')
def cancel_order(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    for item in order.items.all():
        item.product.stock_quantity += item.quantity
        item.product.save()
    order.status = 'Cancelled'
    order.save()
    return JsonResponse({"status": "Cancelled"})


def order_return(request):
    order_id = request.POST.get('order_id')
    text = request.POST.get('text')
    print("order id: ", order_id)
    order = Order.objects.get(id=order_id)
    order.status = 'Returned'
    order.reason = text
    order.save()
    for item in order.items.all():
        item.product.stock_quantity += item.quantity
        item.product.save()
    return JsonResponse({'status': 'Returned'})


def get_coupons(request):
    coupons = Coupon.objects.all()
    coupon_list = [{'code': coupon.code, 'discount_value': coupon.discount_value} for coupon in coupons]
    response = {'coupons': coupon_list}
    return JsonResponse(response)


def apply_coupon(request):
    code = request.GET.get('coupon_code')

    # total_cost = float(request.GET.get('total_cost'))
    total_cost = 0
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        total_cost += item.get_total_cost()

    try:
        coupon = get_object_or_404(Coupon, code=code, active=True, valid_from__lte=timezone.now(),
                                   valid_to__gte=timezone.now())
        if coupon.minimum_purchase and total_cost < coupon.minimum_purchase:
            raise ValidationError('Minimum purchase amount not met')
        if coupon.maximum_discount and coupon.discount_value > coupon.maximum_discount:
            raise ValidationError('Discount exceeds maximum limit')
        discount_amount = coupon.discount_value
        total_cost = float(total_cost) - float(discount_amount)
        request.session['coupon'] = code
        request.session['total_cost'] = total_cost
        response = {
            'success': True,
            'updated_cost': total_cost,
            'discount': discount_amount,
            'messages': 'Coupon applied successfully'
        }
    except (Coupon.DoesNotExist, ValidationError) as e:
        print('im not working')
        response = {
            'success': False,
            'updated_cost': total_cost,
            'messages': str(e)
        }

    return JsonResponse(response)


def delete_coupon(request):
    code = request.session['coupon']
    request.session.pop('coupon', None)
    request.session.pop('total_cost', None)
    request.session.modified = True
    total_cost = 0
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        total_cost += item.get_total_cost()
    response = {
        'success': True,
        'updated_cost': total_cost,
        'messages': 'Coupon deleted successfully'
    }
    return JsonResponse(response)


def generate_invoice(order):
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Set up the invoice content
    # You can customize the content as per your requirements
    p.setFont('Helvetica', 12)
    p.drawString(50, 800, f"Invoice for Order #{order.id}")
    p.drawString(50, 780, f"Customer: {order.user.first_name}")
    p.drawString(50, 760, f"Total Amount: {order.total_price}")

    # Save the PDF content to the buffer
    p.showPage()
    p.save()

    # Get the value of the buffer and create the response
    buffer.seek(0)
    return buffer


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice_content = generate_invoice(order)

    # Set the appropriate content type and headers for the response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.id}.pdf'

    # Write the PDF content to the response
    response.write(invoice_content.getvalue())
    return response


def checkout_buy_now(request):
    print('i am buynow option and i am working')
    global shipping_cost
    discount = 0.00
    product_id = request.GET.get('product_id')
    quantity = request.GET.get('quantity')
    print(product_id, quantity)
    product = get_object_or_404(Product, id=product_id)
    addresses = UserAddress.objects.filter(user=request.user)
    total_cost = float(product.price) * float(quantity)

    if 'coupon' in request.session:
        coupon = request.session['coupon']
        coupon = get_object_or_404(Coupon, code=coupon, active=True, valid_from__lte=timezone.now(),
                                   valid_to__gte=timezone.now())
        discount = coupon.discount_value

    coupons = Coupon.objects.all()
    active_coupon = request.session.get('coupon')
    print(active_coupon, 'i am the active coupon')
    user = request.user
    form = OrderForm()

    context = {
        'addresses': addresses,
        'product': product,
        'quantity': quantity,
        'total_cost': total_cost,
        'user': user,
        'form': form,
        'coupon': coupons,
        'active_coupon': active_coupon,
        'discount': discount

    }
    return render(request, 'checkout_buy_now.html', context)


def buy_now(request):
    if request.method == 'POST':
        print('this is a post method and it is working')

    global shipping_cost
    discount = 0.00
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    print(product_id, quantity)
    product = get_object_or_404(Product, id=product_id)
    addresses = UserAddress.objects.filter(user=request.user)
    total_cost = float(product.price) * float(quantity)
    print(product_id, quantity)
    if request.method == 'POST':
        shipping_options = request.POST.get('shipping_options')
        shipping_address_id = request.POST.get('address')

        if shipping_options == 'free_shipping':
            shipping_cost = 0.00
        elif shipping_options == 'faster_shipping':
            shipping_cost = 100.00

        total_cost += shipping_cost

        payment_method = request.POST['payment_option']
        shipping_address = UserAddress.objects.get(id=shipping_address_id)

        if payment_method == 'razorpay':

            # Create a new order object but do not save it yet
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                status=Order.PENDING,
                total_price=total_cost
            )

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(quantity),
                price=product.price
            )
            order_item.save()

            product.stock_quantity -= int(quantity)
            product.save()

            # Initialize Razorpay client with your account's API key and secret
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Create a Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(total_cost * 100),  # Razorpay amount is in paisa
                'currency': 'INR',
                'payment_capture': '1',  # Auto capture payment
            })

            # Save Razorpay order ID to your order object
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            request.session.pop('coupon', None)
            request.session.modified = True

            # Return Razorpay order ID to the frontend
            return JsonResponse({'razorpay_order_id': razorpay_order['id']})
        else:
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                status=Order.PENDING,
                total_price=total_cost
            )

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(quantity),
                price=product.price
            )
            order_item.save()

            product.stock_quantity -= int(quantity)
            product.save()

            order.save()
            request.session.pop('coupon', None)
            request.session.modified = True

            return redirect('cart:order_list')


def apply_coupon_buy_now(request):
    code = request.GET.get('coupon_code')
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))

    try:
        product = get_object_or_404(Product, id=product_id)
        total_cost = product.price * quantity

        coupon = get_object_or_404(Coupon, code=code, active=True, valid_from__lte=timezone.now(),
                                   valid_to__gte=timezone.now())

        if coupon.minimum_purchase and total_cost < coupon.minimum_purchase:
            raise ValidationError('Minimum purchase amount not met')

        if coupon.maximum_discount and coupon.discount_value > coupon.maximum_discount:
            raise ValidationError('Discount exceeds maximum limit')

        discount_amount = coupon.discount_value
        total_cost -= discount_amount

        request.session['coupon'] = code
        request.session['total_cost'] = total_cost

        response = {
            'success': True,
            'updated_cost': total_cost,
            'discount': discount_amount,
            'message': 'Coupon applied successfully'
        }
    except (Product.DoesNotExist, Coupon.DoesNotExist, ValidationError) as e:
        response = {
            'success': False,
            'updated_cost': total_cost,
            'message': str(e)
        }

    return JsonResponse(response)


def proceed_to_pay_buy_now(request):
    global shipping_cost, discount
    total_price = 0
    discount = 0.00

    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))
    print(product_id, quantity, 'proceed to pay buy no working ferfect')

    try:
        product = get_object_or_404(Product, id=product_id)

        total_price = float(product.price) * float(quantity)

        if 'total_cost' in request.session:
            total_price = request.session['total_cost']

        if request.GET.get('shipping_options'):
            shipping_options = request.GET.get('shipping_options')
            if shipping_options == 'free_shipping':
                shipping_cost = 0.00
            elif shipping_options == 'faster_shipping':
                shipping_cost = 100.00

            if 'total_cost' in request.session:
                total_price = request.session['total_cost']
                total_price += float(shipping_cost)
            else:
                total_price += float(shipping_cost)

        if 'coupon' in request.session:
            coupon = request.session['coupon']
            coupon = get_object_or_404(Coupon, code=coupon, active=True, valid_from__lte=timezone.now(),
                                       valid_to__gte=timezone.now())
            discount = coupon.discount_value

        total_price = round(total_price)

        response = {
            'total_price': total_price,
            'shipping_cost': shipping_cost,
            'discount': discount,
        }
    except (Product.DoesNotExist, Coupon.DoesNotExist) as e:
        response = {
            'error': str(e)
        }

    return JsonResponse(response)
