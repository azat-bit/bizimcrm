from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from .models import CustomerCategory

def create_category(request):
    if request.method == "POST":
        # Form verilerini doğrudan POST'dan alıyoruz
        name = request.POST.get("name", "").strip()

        errors = {}
        if not name:
            errors["name"] = "Kategori adı boş bırakılamaz."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            category = CustomerCategory.objects.create(name=name)
        except IntegrityError:
            errors["name"] = "Bu kategori adı zaten kayıtlı."
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Başarılı kayıt durumunda JSON yanıt döndür
        return JsonResponse({
            'status': 'success',
            'message': 'Kategori başarıyla eklendi.',
            'category': {
                'id': category.id,
                'name': category.name,
            }
        })
    else:
        # GET isteğinde form sayfasını render et
        return render(request, 'crm/create_category.html')
    

def list_categories(request):
    categories = CustomerCategory.objects.all()
    return render(request, 'crm/list_categories.html', {'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(CustomerCategory, id=category_id)
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        errors = {}
        if not name:
            errors["name"] = "Kategori adı boş bırakılamaz."
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        try:
            category.name = name
            category.save()
        except IntegrityError:
            errors["name"] = "Bu kategori adı zaten kayıtlı."
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        return JsonResponse({
            'status': 'success',
            'message': 'Kategori başarıyla güncellendi.',
            'category': {
                'id': category.id,
                'name': category.name,
            }
        })
    else:
        return render(request, 'crm/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(CustomerCategory, id=category_id)
    category.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Kategori başarıyla silindi.',
    })