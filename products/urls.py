# products/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name ထည့်ပေးရပါမယ် (core/urls.py မှာ namespace='products' သုံးထားလို့ ဖြစ်ပါတယ်)
app_name = 'products'

urlpatterns = [
    # Admin Dashboard URL
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Product CRUD URLs
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Category CRUD URLs
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Subcategory CRUD URLs
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    
    # Cashier CRUD URLs
    path('cashier/add/', views.add_cashier, name='add_cashier'),
    path('cashier/edit/<int:cashier_id>/', views.edit_cashier, name='edit_cashier'),
    path('cashier/delete/<int:cashier_id>/', views.delete_cashier, name='delete_cashier'),
    
    path('api/get-scanned-code/', views.get_scanned_code, name='get_scanned_code'),
    # path('api/scan-product/', views.scan_product_api, name='scan_product_api'),
    
    # ⚠️ ဤလိုင်းအသစ်ကို ထည့်ပေးပါ
    path('cashier-login/', views.cashier_login, name='cashier_login'),
    
    # ⚠️ Cashier အရောင်းစာမျက်နှာအတွက် ဤလိုင်းကို ထည့်ပေးပါ
    path('pos-terminal/', views.pos_page, name='pos_page'),
    path('api/scan-product/<str:product_code>/', views.scan_product_api, name='scan_product_api'),
    
    # Supplier CRUD URLs
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    
    # Size CRUD URLs
    path('sizes/add/', views.add_size, name='add_size'),
    path('sizes/edit/<int:size_id>/', views.edit_size, name='edit_size'),
    path('sizes/delete/<int:size_id>/', views.delete_size, name='delete_size'),
    
    # Variant CRUD URLs
    path('variants/add/', views.add_variant, name='add_variant'),
    path('variants/delete/<int:variant_id>/', views.delete_variant, name='delete_variant'),

    # Purchase CRUD URLs
    path('purchases/add/', views.add_purchase, name='add_purchase'),
    path('purchases/delete/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),

]