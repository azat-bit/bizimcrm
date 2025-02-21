from django.db import models

class CustomerCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('individual', 'Bireysel'),
        ('corporate', 'Kurumsal'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class CustomerInteraction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    interaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField()
    interaction_type = models.CharField(max_length=50, choices=[
        ('call', 'Telefon Görüşmesi'),
        ('email', 'E-posta'),
        ('meeting', 'Toplantı'),
    ])

    def __str__(self):
        return f"{self.customer.name} - {self.interaction_type}"

class CustomerFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.customer.name} - {self.rating}⭐"
