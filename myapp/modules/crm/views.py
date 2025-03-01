from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, CustomerCategory
from django.http import HttpResponse
from django.urls import reverse

from django.http import JsonResponse
from django.db import IntegrityError

# Müşteri Listeleme
def customer_list(request):
    query = request.GET.get('q', '')  # Arama terimini al
    if query:
        customers = Customer.objects.filter(name__icontains=query)  # İsme göre filtrele
    else:
        customers = Customer.objects.all()  # Arama yoksa tüm müşterileri getir
    
    return render(request, 'crm/customer_list.html', {'customers': customers})

# Müşteri Detay Sayfası
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)  # Müşteri detaylarını al
    return render(request, 'crm/customer_detail.html', {'customer': customer})

# Müşteri Ekleme
def new_customer(request):
    
    if request.method == "POST":
        # Form verilerini doğrudan POST'dan alıyoruz
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        errors = {}
        if not name:
            errors["name"] = "İsim alanı boş bırakılamaz."
        if not email:
            errors["email"] = "E-posta alanı boş bırakılamaz."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address
            )
        except IntegrityError as e:
            # IntegrityError yakalandığında, duplicate entry kontrolü yapalım
            error_message = str(e)
            if "Duplicate entry" in error_message and "for key 'email'" in error_message:
                errors["email"] = "Bu e-posta adresi zaten kayıtlı."
            else:
                errors["non_field_error"] = "Bir hata oluştu, lütfen tekrar deneyin."
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Başarılı kayıt durumunda JSON yanıt döndür
        return JsonResponse({
            'status': 'success',
            'message': 'Müşteri başarıyla eklendi.',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address,
            }
        })
    else:
        # GET isteğinde form sayfasını render et
        return render(request, 'crm/customer_create.html')

# Müşteri Düzenleme

def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)  # Müşteriyi bul
    categories = CustomerCategory.objects.all()  # Tüm kategorileri çek

    if request.method == "POST":
        # Form verilerini işle
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        category_id = request.POST.get("category", "").strip()

        errors = {}
        if not name:
            errors["name"] = "İsim alanı boş bırakılamaz."
        if not email:
            errors["email"] = "E-posta alanı boş bırakılamaz."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            category = CustomerCategory.objects.get(id=category_id) if category_id else None
            customer.name = name
            customer.email = email
            customer.phone = phone
            customer.address = address
            customer.category = category
            customer.save()
        except IntegrityError:
            errors["email"] = "Bu e-posta adresi zaten kayıtlı."
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        return JsonResponse({
            'status': 'success',
            'message': 'Müşteri başarıyla güncellendi.',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address,
                'category': customer.category.name if customer.category else None,
            }
        })
    else:
        # GET isteğinde form sayfasını render et
        return render(request, 'crm/customer_edit.html', {
            'customer': customer,
            'categories': categories,
        })