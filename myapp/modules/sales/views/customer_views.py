from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Customer
  # veya relative: from ..models import Customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customers.html', {'customers': customers})
  # Relative import, dosya yapınıza göre ayarlayın

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
        return render(request, 'customer/create_customer.html')
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    
    if request.method == "POST":
        # Form verilerini POST'dan alıyoruz
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
            customer.name = name
            customer.email = email
            customer.phone = phone
            customer.address = address
            customer.save()
        except IntegrityError as e:
            error_message = str(e)
            if "Duplicate entry" in error_message and "for key 'email'" in error_message:
                errors["email"] = "Bu e-posta adresi zaten kayıtlı."
            else:
                errors["non_field_error"] = "Bir hata oluştu, lütfen tekrar deneyin."
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
            }
        })
    else:
        # GET isteğinde düzenleme sayfasını, mevcut müşteri verileriyle birlikte render ediyoruz
        return render(request, 'customer/edit_customer.html', {'customer': customer})
    

def delete_customer(request, customer_id):
    # GET isteği ile doğrudan silme işlemi yapılıyor
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('sales:customers')