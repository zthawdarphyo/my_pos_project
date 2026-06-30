from django.urls import path
from . import views

urlpatterns = [
    path('pos/', views.pos_dashboard, name='pos_dashboard'),
    path('api/add-to-cart/', views.add_to_cart_api, name='add_to_cart_api'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/save-invoice/', views.save_invoice_api, name='save_invoice_api'),
    # path('api/scan-product/', views.scan_product_api, name='scan_product_api'),

]