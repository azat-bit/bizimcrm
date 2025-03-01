from django.urls import path
from . import customer_views ,views,category_views # customer_views.py dosyasını import ediyoruz


app_name = "crm"

urlpatterns = [
    
    path('', customer_views.crm_home, name='crm_home'),
    
    
    path('customers/', customer_views.customer_list, name='customers'),
    path('customers/new/', customer_views.new_customer, name='new_customer'),
    path('customers/<int:customer_id>/edit/', customer_views.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', customer_views.delete_customer, name='delete_customer'),
    path('create-category/', category_views.create_category, name='create_category'),
    path('category/', category_views.list_categories, name='list_categories'),
    path('category/<int:category_id>/edit/', category_views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', category_views.delete_category, name='delete_category'),
    path('search-customers/', customer_views.search_customers, name='search_customers'),
    path('export-customers-excel/', customer_views.export_customers_excel, name='export_customers_excel'),
]
