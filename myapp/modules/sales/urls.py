from django.urls import path
from .views import index, customer_list, product_list,customer_views,edit_customer

app_name = "sales"

urlpatterns = [
    path('', index, name='index'),
    path('customers/', customer_list, name='customers'),
    path('customers/new/', customer_views.new_customer, name='new_customer'),
    path('customers/<int:customer_id>/edit/', customer_views.edit_customer, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', customer_views.delete_customer, name='delete_customer'),
    path('products/', product_list, name='products'),
]