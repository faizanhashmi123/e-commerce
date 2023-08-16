from django.db import models
from apps.customer.models import Customer
from apps.product.models import Product
from apps.user.models import User
from application.custom_models import DateTimeModel
from django.utils import timezone


class Cart(DateTimeModel):
    owner = models.ForeignKey(Customer,  on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class Order(DateTimeModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(DateTimeModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Checkout(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    items = models.ManyToManyField(Product, through='CheckoutItem')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)  # e.g., Credit Card, PayPal, etc.
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Checkout #{self.pk}"


class CheckoutItem(DateTimeModel):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - ${self.price}"


class Coupon(DateTimeModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    minimum_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_usage_count = models.PositiveIntegerField(default=1)
    times_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.item.name



