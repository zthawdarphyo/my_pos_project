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
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Cashier CRUD URLs
    path('cashier/add/', views.add_cashier, name='add_cashier'),
    path('cashier/delete/<int:cashier_id>/', views.delete_cashier, name='delete_cashier'),
    
    path('api/get-scanned-code/', views.get_scanned_code, name='get_scanned_code'),
    # path('api/scan-product/', views.scan_product_api, name='scan_product_api'),
    
    # ⚠️ ဤလိုင်းအသစ်ကို ထည့်ပေးပါ
    path('cashier-login/', views.cashier_login, name='cashier_login'),
    
    # ⚠️ Cashier အရောင်းစာမျက်နှာအတွက် ဤလိုင်းကို ထည့်ပေးပါ
    path('pos-terminal/', views.pos_page, name='pos_page'),
    path('api/scan-product/<str:product_code>/', views.scan_product_api, name='scan_product_api'),
  
]