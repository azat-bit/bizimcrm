from django.db import models
from myapp.modules.crm.models import Customer

class MarketingCampaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    platform = models.CharField(max_length=50, choices=[
        ('social_media', 'Sosyal Medya'),
        ('email', 'E-Posta'),
        ('google_ads', 'Google Ads'),
    ])

    def __str__(self):
        return self.name

class CustomerSegment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    customers = models.ManyToManyField(Customer, blank=True)

    def __str__(self):
        return self.name

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField()
    expiration_date = models.DateField()
    
    def __str__(self):
        return f"{self.code} - %{self.discount_percentage} indirim"
