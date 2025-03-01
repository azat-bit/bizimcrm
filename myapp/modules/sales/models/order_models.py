from django.db import models
from myapp.modules.crm.models import Customer
from myapp.modules.inventory.models import Product

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Beklemede'),
            ('processing', 'İşleniyor'),
            ('shipped', 'Kargolandı'),
            ('delivered', 'Teslim Edildi'),
        ]
    )

    def __str__(self):
        return f"Sipariş {self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Sipariş {self.order.id})"

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Hazırlanıyor'),
            ('shipped', 'Kargoya Verildi'),
            ('delivered', 'Teslim Edildi'),
        ]
    )

    def __str__(self):
        return f"Kargo {self.tracking_number} - {self.order.customer.name}"
