from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from .models import Customer, CustomerCategory
from openpyxl import Workbook

  # veya relative: from ..models import Customer


# customer_views.py


def crm_home(request):
    customers = Customer.objects.all()
    return render(request, 'crm/anasayfa.html', {'customers': customers})



def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'crm/customer.html', {'customers': customers})
  # Relative import, dosya yapınıza göre ayarlayın


def new_customer(request):
    if request.method == "POST":
        # Form verilerini doğrudan POST'dan alıyoruz
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
            category = None
            if category_id:
                category = CustomerCategory.objects.get(id=category_id)

            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                category=category
            )
        except IntegrityError as e:
            # IntegrityError yakalandığında, duplicate entry kontrolü yapalım
            error_message = str(e)
            if "Duplicate entry" in error_message and "for key 'email'" in error_message:
                errors["email"] = "Bu e-posta adresi zaten kayıtlı."
            else:
                errors["non_field_error"] = "Bir hata oluştu, lütfen tekrar deneyin."
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        except CustomerCategory.DoesNotExist:
            errors["category"] = "Geçersiz kategori seçimi."
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
                'category': customer.category.name if customer.category else None,
            }
        })
    else:
        # GET isteğinde form sayfasını render et
        categories = CustomerCategory.objects.all()
        return render(request, 'crm/create_customer.html', {'categories': categories})

    

def delete_customer(request, customer_id):
    # GET isteği ile doğrudan silme işlemi yapılıyor
    customer = get_object_or_404(Customer, pk=customer_id)
    customer.delete()
    return redirect('crm:customers')



def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    categories = CustomerCategory.objects.all()

    if request.method == "POST":
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
        return render(request, 'crm/edit_customer.html', {
            'customer': customer,
            'categories': categories,
        })
    
def search_customers(request):
    search_query = request.GET.get('search_query', '').strip().lower()  # Arama sorgusunu al
    if search_query:
        # İsme göre müşterileri filtrele
        customers = Customer.objects.filter(name__icontains=search_query)
    else:
        # Eğer arama sorgusu yoksa tüm müşterileri getir
        customers = Customer.objects.all()

    # Filtrelenmiş müşterileri HTML olarak render et
    return render(request, 'crm/customer_table.html', {'customers': customers})


def export_customers_excel(request):
    # Müşteri bilgilerini veritabanından çek
    customers = Customer.objects.all()

    # Yeni bir Excel çalışma kitabı oluştur
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Müşteriler"

    # Başlık satırını ekle
    worksheet.append(["ID", "İsim", "E-Posta", "Telefon", "Adres"])

    # Müşteri bilgilerini Excel'e ekle
    for customer in customers:
        worksheet.append([
            customer.id,
            customer.name,
            customer.email,
            customer.phone,
            customer.address
        ])

    # HttpResponse oluştur ve Excel dosyasını ekle
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="musteriler.xlsx"'
    workbook.save(response)

    return response