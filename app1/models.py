from django.db import models
from django.contrib.auth.models import User

# Bảng lưu thông tin khách hàng
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Liên kết một đối một với bảng User
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Số điện thoại khách hàng

    def __str__(self):
        return f"Khách hàng: {self.user.username}"

# Bảng lưu thông tin địa chỉ giao hàng của khách hàng
class ShoppingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Liên kết với khách hàng
    address = models.CharField(max_length=255)  # Địa chỉ giao hàng
    city = models.CharField(max_length=100)  # Thành phố
    phone = models.CharField(max_length=100)  # Mã bưu chính
    country = models.CharField(max_length=100)  # Quốc gia
    date = models.DateTimeField(auto_created=True)
    def __str__(self):
        return f"Địa chỉ giao hàng: {self.address}, {self.city}"

# Bảng lưu thông tin sản phẩm
# app1/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to='products/', default='products/default.jpg')  # Đảm bảo có default
    description = models.TextField()

    def __str__(self):
        return self.name


# Bảng giỏ hàng của khách hàng
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Liên kết với khách hàng
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo giỏ hàng

    def __str__(self):
        return f"Giỏ hàng của {self.customer.user.username}"

# Bảng lưu thông tin sản phẩm trong giỏ hàng
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Liên kết với giỏ hàng
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Sản phẩm trong giỏ
    quantity = models.IntegerField(default=1)  # Số lượng sản phẩm

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Bảng đơn hàng của khách hàng
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Thiết lập giá trị mặc định
    shipping_address = models.ForeignKey(ShoppingAddress, on_delete=models.SET_NULL, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Đơn hàng {self.id} của {self.customer.user.username}"

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum(item.quantity for item in order_items)
        return total

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum(item.get_total() for item in order_items) 
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} trong đơn hàng {self.order.id}"

    def get_total(self):
     return self.product.price * self.quantity

