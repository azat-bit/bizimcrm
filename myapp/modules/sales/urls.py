from django.urls import path
from . import views  # views.py dosyanın var olduğundan emin ol

app_name = "sales"

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customer_list, name='customers'),
    path('products/', views.product_list, name='products'),
]