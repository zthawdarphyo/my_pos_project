# products/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name ထည့်ပေးရပါမယ် (core/urls.py မှာ namespace='products' သုံးထားလို့ ဖြစ်ပါတယ်)
app_name = 'products'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/overview/', views.admin_dashboard, {'section': 'dashboard'}, name='admin_dashboard_overview'),
    path('dashboard/products/', views.admin_dashboard, {'section': 'products'}, name='admin_dashboard_products'),
    path('dashboard/cashiers/', views.admin_dashboard, {'section': 'cashiers'}, name='admin_dashboard_cashiers'),
    path('dashboard/categories/', views.admin_dashboard, {'section': 'categories'}, name='admin_dashboard_categories'),
    path('dashboard/subcategories/', views.admin_dashboard, {'section': 'subcategories'}, name='admin_dashboard_subcategories'),
    path('dashboard/reports/', views.admin_dashboard, {'section': 'reports'}, name='admin_dashboard_reports'),
    path('dashboard/suppliers/', views.admin_dashboard, {'section': 'suppliers'}, name='admin_dashboard_suppliers'),
    path('dashboard/purchases/', views.admin_dashboard, {'section': 'purchase'}, name='admin_dashboard_purchases'),
    path('dashboard/sizes/', views.admin_dashboard, {'section': 'size'}, name='admin_dashboard_sizes'),
    path('dashboard/variants/', views.admin_dashboard, {'section': 'variant'}, name='admin_dashboard_variants'),
    path('dashboard/balance/', views.admin_dashboard, {'section': 'balance'}, name='admin_dashboard_balance'),
    path('dashboard/management/', views.admin_dashboard, {'section': 'management'}, name='admin_dashboard_management'),
    path('dashboard/settings/', views.admin_dashboard, {'section': 'settings'}, name='admin_dashboard_settings'),
    
    # Product CRUD URLs
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # ManagedProduct CRUD URLs (Product Management tab - independent)
    path('managed-products/add/', views.add_managed_product, name='add_managed_product'),
    path('managed-products/edit/<int:managed_product_id>/', views.edit_managed_product, name='edit_managed_product'),
    path('managed-products/delete/<int:managed_product_id>/', views.delete_managed_product, name='delete_managed_product'),
    
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
    path('variants/edit/<int:variant_id>/', views.edit_variant, name='edit_variant'),
    path('variants/delete/<int:variant_id>/', views.delete_variant, name='delete_variant'),

    # Purchase CRUD URLs
    path('purchases/add/', views.add_purchase, name='add_purchase'),
    path('purchases/edit/<int:purchase_id>/', views.edit_purchase, name='edit_purchase'),
    path('purchases/delete/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),

]