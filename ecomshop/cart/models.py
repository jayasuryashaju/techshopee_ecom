from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product, Category
from user_profile.models import UserAddress


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} added by {self.user.username}'

    # def get_total_cost(self):
    #     return self.product.price * self.quantity
    def get_total_cost(self):
        if self.product.selling_price:
            return self.product.selling_price * self.quantity
        else:
            return self.product.price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    maximum_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=1000, null=True)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Payment options
    CASH_ON_DELIVERY = 'cash_on_delivery'
    RAZORPAY = 'Razorpay'
    PAYMENT_CHOICES = [
        (CASH_ON_DELIVERY, 'Cash on delivery'),
        (RAZORPAY, 'Razorpay')
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=CASH_ON_DELIVERY)

    # Order status
    PENDING = 'pending'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (RETURNED, 'Returned')
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Order {self.id} - {self.user}'

    # def save(self, *args, **kwargs):
    #     self.total_price = self.get_total_cost()
    #     super().save(*args, **kwargs)

    def get_total_cost(self):
        return self.product.price * self.quantity


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     def __str__(self):
#         return f'{self.quantity} x {self.product.name}'
#
#     def get_item_price(self):
#         return self.product.price * self.quantity

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_item_price(self):
        return self.product.price * self.quantity


class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
