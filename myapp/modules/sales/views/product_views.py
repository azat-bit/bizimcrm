from django.shortcuts import render
from ..models import ProductModels # veya relative: from ..models import Product

def product_list(request):
    products = ProductModels.objects.all()
    return render(request, 'products.html', {'products': products})
