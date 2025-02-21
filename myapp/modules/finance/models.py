from django.db import models
from myapp.modules.crm.models import Customer
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ödeme Bekleniyor'),
        ('paid', 'Ödendi'),
        ('overdue', 'Vadesi Geçti'),
    ])

    def __str__(self):
        return f"Fatura {self.id} - {self.customer.name}"

class Payment(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Kredi Kartı'),
        ('bank_transfer', 'Banka Havalesi'),
        ('cash', 'Nakit'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ödeme {self.amount} - {self.payment_method}"
