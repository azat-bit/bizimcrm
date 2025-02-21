from django.shortcuts import render
from .models import Customer, Product

def index(request):
    return render(request, 'anasayfa.html') 

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
