from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/', views.pos_dashboard, name='pos_dashboard'),
    path('api/add-to-cart/', views.add_to_cart_api, name='add_to_cart_api'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/save-invoice/', views.save_invoice_api, name='save_invoice_api'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:order_id>/', views.invoice_detail, name='invoice_detail'),
    path('sale-invoices/<int:sale_id>/', views.sale_invoice, name='sale_invoice'),
]