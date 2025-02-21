from django.db import models
from myapp.modules.sales.models import Order
from myapp.modules.crm.models import Customer

class SalesAnalytics(models.Model):
    report_date = models.DateField(auto_now_add=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    top_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Satış Raporu - {self.report_date}"

class CustomerBehaviorAnalytics(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_orders = models.PositiveIntegerField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    last_order_date = models.DateField()

    def __str__(self):
        return f"{self.customer.name} - {self.total_orders} sipariş"

class PerformanceReports(models.Model):
    report_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()

    def __str__(self):
        return self.report_name
