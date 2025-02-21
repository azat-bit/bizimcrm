from django.shortcuts import render
from django.conf import settings

def home(request):
    modules = [
        {"name": "Analytics", "url": "/analytics/", "img": "/static/img/analytics.jpg"},
        {"name": "CRM", "url": "/crm/", "img": "/static/img/crm.webp"},
        {"name": "Finance", "url": "/finance/", "img": "/static/img/finance.webp"},
        {"name": "HR", "url": "/hr/", "img": "/static/img/hr.webp"},
        {"name": "Inventory", "url": "/inventory/", "img": "/static/img/inventory.webp"},
        {"name": "Marketing", "url": "/marketing/", "img": "/static/img/marketing.webp"},
        {"name": "Project A", "url": "/projectA/", "img": "/static/img/projectA.webp"},
        {"name": "Project B", "url": "/projectB/", "img": "/static/img/projectB.webp"},
        {"name": "Project C", "url": "/projectC/", "img": "/static/img/projectC.webp"},
        {"name": "Sales", "url": "/sales/", "img": "/static/img/sales.webp"},
    ]
    
    return render(request, "index.html", {"modules": modules})
