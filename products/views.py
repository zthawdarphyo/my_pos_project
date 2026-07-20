
import json
import qrcode
from io import BytesIO
from decimal import Decimal

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


from django.core.files import File


from .models import Product, Category, Subcategory, Supplier, ProductSize, ProductVariant, CashierProfile, Purchase
from sales.models import Order, OrderItem

# products/views.py ထဲက အပိုင်း

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product 

def cashier_login(request):
    if request.user.is_authenticated:
        # အကယ်၍ Login ဝင်ထားပြီးသား ဖြစ်နေရင် Role အလိုက် ပြန်ပို့ပေးမယ်
        if request.user.is_staff or request.user.is_superuser:
            return redirect('products:admin_dashboard')
        else:
            return redirect('products:pos_page') # Cashier အတွက် အရောင်းစာမျက်နှာ
        
    if request.method == "POST":
        user_input = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=user_input, password=password)
        if user is not None:
            login(request, user)
            
            # 👑 ဝင်လာတဲ့ User က Admin (Staff) ဖြစ်နေလျှင်
            if user.is_staff or user.is_superuser:
                return redirect('products:admin_dashboard') # Admin Dashboard သို့ သွားမည်
            
            # 🛒 ဝင်လာတဲ့ User က သာမန် Cashier ဖြစ်နေလျှင်
            else:
                return redirect('products:pos_page') # POS အရောင်းစာမျက်နှာ သို့ သွားမည်
                
        else:
            return render(request, 'products/cashier_pos.html', {'error': True})
            
    return render(request, 'products/cashier_pos.html')


# ⚠️ Cashier ရောက်မည့် POS Page အတွက် View အသစ် (မရှိသေးရင် အောက်ဆုံးမှာ ထပ်ထည့်ပေးပါ)
def pos_page(request):
    # ဒီနေရာမှာ Database ထဲက Products တွေကို ဆွဲထုတ်ပြီး ရောင်းမယ့် UI ကို ပို့ပေးမယ်
    return render(request, 'products/pos_invoice.html')
@login_required
# def get_product_by_barcode(request, barcode):
#     # Scanner က ဖတ်လိုက်တဲ့ Barcode ကို Database ထဲမှာ Admin ထည့်ထားသလား ရှာဖွေခြင်း
#     try:
#         product = Product.objects.get(barcode=barcode)
#         return JsonResponse({
#             'success': True,
#             'name': product.name,
#             'price': float(product.price)
#         })
#     except Product.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'Product not found'})
# 🔄 products/views.py ထဲက အဟောင်းနေရာမှာ ဤ API ကုဒ်ကို အစားထိုးပါ

# products/views.py ထဲရှိ scan_product_api ကို ဤကုဒ်ဖြင့် လဲလှယ်ပါ

def scan_product_api(request, product_code):
    """
    URL မှ ပါလာသော product_code ကို လက်ခံပြီး Database တွင် ရှာဖွေပေးမည့် API
    """
    code = product_code.strip()
    
    try:
        # သင့် Model ၏ field အမည် product_code အတိုင်း စစ်ဆေးရှာဖွေခြင်း
        product = Product.objects.get(product_code=code)
        
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price)
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': f'ကုန်ပစ္စည်း ကုဒ် [{code}] အား ရှာမတွေ့ပါ။'
        })
        
        
def save_transaction(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get('cart', [])
        
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
            
        # တကယ့် Database (MySQL) ထဲသို့ အရောင်းစာရင်း သွားသိမ်းခြင်း
        # txn = Transaction.objects.create(cashier=request.user, total=data.get('total'))
        # စသည်ဖြင့် သင့် Model အတိုင်း သိမ်းဆည်းနိုင်ပါသည်
        
        return JsonResponse({'success': True})

# Session အစား လုံးဝ သေချာသွားအောင် Global variable နဲ့ ခေတ္တ စမ်းသပ်ပါမယ်
# LATEST_SCAN_CODE = None

# @csrf_exempt
# def scan_product_api(request):
#     global LATEST_SCAN_CODE
#     if request.method == "POST":
#         product_code = request.POST.get('product_code', '').strip()
#         if product_code:
#             LATEST_SCAN_CODE = product_code  # ကုဒ်ကို သိမ်းလိုက်ပြီ
#             print(f"--- [Server] ကင်မရာမှ ကုဒ်ဖတ်မိ၍ သိမ်းလိုက်ပါပြီ: {product_code} ---")
#             return JsonResponse({"status": "success", "code": product_code})
            
#     return JsonResponse({"status": "error"}, status=400)


def get_scanned_code(request):
    global LATEST_SCAN_CODE
    if LATEST_SCAN_CODE:
        temp_code = LATEST_SCAN_CODE
        LATEST_SCAN_CODE = None  # ယူပြီးရင် တစ်ခါတည်း ပြန်ဖျက်မယ်
        print(f"--- [Server] Browser သို့ ကုဒ် လှမ်းပေးလိုက်ပါပြီ: {temp_code} ---")
        return JsonResponse({"code": temp_code})
        
    return JsonResponse({"code": None})


def admin_dashboard(request):
    from django.utils import timezone as _tz
    today = _tz.localtime(_tz.now()).date()

    products_list = Product.objects.all()
    categories = Category.objects.all()
    cashiers_list = User.objects.filter(is_superuser=False).select_related('cashier_profile')
    suppliers = Supplier.objects.all()
    sizes = ProductSize.objects.all()
    variants = ProductVariant.objects.all()
    subcategories = Subcategory.objects.all()

    today_orders = Order.objects.filter(created_at__date=today)
    today_items = OrderItem.objects.filter(order__in=today_orders)
    today_sales = today_items.aggregate(total=models.Sum(models.F('quantity') * models.F('price')))['total'] or 0
    today_transactions = today_orders.count()
    low_stock_count = products_list.filter(stock__lt=10).count()

    total_revenue = OrderItem.objects.aggregate(total=models.Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_expenses = 0
    net_balance = total_revenue - total_expenses

    total_products = products_list.count()
    total_categories = categories.count()
    total_suppliers = suppliers.count()

    purchase_orders = Purchase.objects.all().order_by('-created_at')

    purchase_paginator = Paginator(purchase_orders, 4)
    purchase_page = purchase_paginator.get_page(request.GET.get('purchase_page'))
    _pur_total_pages = purchase_paginator.num_pages
    _pur_start = purchase_page.number
    if _pur_start > _pur_total_pages - 1:
        _pur_start = max(1, _pur_total_pages - 1)
    purchase_page_range = range(_pur_start, min(_pur_start + 1, _pur_total_pages) + 1)

    balance_entries = []

    start_date = request.GET.get('start_date', '')
    search_month = request.GET.get('search_month', '')
    search_year = request.GET.get('search_year', '')
    cashier_filter = request.GET.get('cashier_filter', 'all')
    product_filter = request.GET.get('product_filter', 'all')

    report_orders = Order.objects.all()

    if start_date:
        report_orders = report_orders.filter(created_at__date__gte=start_date)
    if search_month:
        try:
            year, month = search_month.split('-')
            report_orders = report_orders.filter(created_at__year=year, created_at__month=month)
        except ValueError:
            pass
    if search_year:
        report_orders = report_orders.filter(created_at__year=search_year)
    if cashier_filter != 'all':
        report_orders = report_orders.filter(cashier_id=cashier_filter)

    report_items = OrderItem.objects.filter(order__in=report_orders).select_related('product', 'order', 'order__cashier')
    if product_filter != 'all':
        report_items = report_items.filter(product_id=product_filter)

    total_report_sales = report_items.aggregate(total=Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_report_trans = report_items.values('order').distinct().count()

    subcategory_paginator = Paginator(subcategories, 4)
    subcategory_page = subcategory_paginator.get_page(request.GET.get('subcat_page'))
    _sub_total_pages = subcategory_paginator.num_pages
    _sub_start = subcategory_page.number
    if _sub_start > _sub_total_pages - 1:
        _sub_start = max(1, _sub_total_pages - 1)
    subcategory_page_range = range(_sub_start, min(_sub_start + 1, _sub_total_pages) + 1)

    size_paginator = Paginator(sizes, 4)
    size_page = size_paginator.get_page(request.GET.get('size_page'))
    _size_total_pages = size_paginator.num_pages
    _size_start = size_page.number
    if _size_start > _size_total_pages - 1:
        _size_start = max(1, _size_total_pages - 1)
    size_page_range = range(_size_start, min(_size_start + 1, _size_total_pages) + 1)

    context = {
        'products': products_list,
        'categories': categories,
        'cashiers': cashiers_list,
        'suppliers': suppliers,
        'sizes': sizes,
        'size_page': size_page,
        'size_page_range': size_page_range,
        'variants': variants,
        'subcategories': subcategories,
        'subcategory_page': subcategory_page,
        'subcategory_page_range': subcategory_page_range,

        'today_sales': today_sales,
        'today_transactions': today_transactions,
        'low_stock_count': low_stock_count,

        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_balance': net_balance,

        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,

        'purchase_orders': purchase_orders,
        'purchase_page': purchase_page,
        'purchase_page_range': purchase_page_range,
        'balance_entries': balance_entries,
        
        'report_items': report_items,
        'total_report_sales': total_report_sales,
        'total_report_trans': total_report_trans,
        
        'start_date': start_date,
        'search_month': search_month,
        'search_year': search_year,
        'cashier_filter': cashier_filter,
        'product_filter': product_filter,
        
        'active_tab': request.GET.get('tab', 'dashboard')
    }
    return render(request, 'products/admin_dashboard.html', context)

# ================= 2. PRODUCT CRUD VIEWS =================
def add_product(request):
    if request.method == "POST":
        p_code = request.POST.get('product_code', '').strip()
        p_name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')

        product = Product(
            name=p_name,
            price=price,
            stock=stock,
            category_id=category
        )

        if p_code:
            product.product_code = p_code
        else:
            generated_code = f"POS-{uuid.uuid4().hex[:8].upper()}" 
            product.product_code = generated_code
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(generated_code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            if hasattr(product, 'qr_code'):
                product.qr_code.save(f"{generated_code}.png", File(buffer), save=False)
            elif hasattr(product, 'qr_image'):
                product.qr_image.save(f"{generated_code}.png", File(buffer), save=False)

        product.save()
        return redirect('/products/dashboard/?tab=products')

    return redirect('/products/dashboard/?tab=products')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.product_code = request.POST.get('product_code')
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)
        
        product.save()
        return redirect('/products/dashboard/?tab=products')
    return redirect('/products/dashboard/?tab=products')

def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
    return redirect('/products/dashboard/?tab=products')


# ================= 3. CATEGORY CRUD VIEWS =================
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
    return redirect('/products/dashboard/?tab=categories')


def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return redirect('/products/dashboard/?tab=categories')


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
    return redirect('/products/dashboard/?tab=categories')


# ================= 3.1 SUBCATEGORY CRUD VIEWS =================
def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, id=category_id)
            Subcategory.objects.create(name=name, category=category)
    return redirect('/products/dashboard/?tab=subcategories')


def delete_subcategory(request, subcategory_id):
    if request.method == 'POST':
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        subcategory.delete()
    return redirect('/products/dashboard/?tab=subcategories')


def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, id=category_id)
            subcategory.name = name
            subcategory.category = category
            subcategory.save()
    return redirect('/products/dashboard/?tab=subcategories')


# ================= 4. CASHIER CRUD VIEWS =================
def add_cashier(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')
        
        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            CashierProfile.objects.create(user=user, phone=phone)
    return redirect('/products/dashboard/?tab=cashiers')


def edit_cashier(request, cashier_id):
    cashier = get_object_or_404(User, id=cashier_id)
    if request.method == 'POST':
        cashier.username = request.POST.get('username')
        cashier.email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        
        profile, created = CashierProfile.objects.get_or_create(user=cashier)
        profile.phone = phone
        profile.save()
        
        cashier.save()
    return redirect('/products/dashboard/?tab=cashiers')


def delete_cashier(request, cashier_id):
    if request.method == 'POST':
        cashier = get_object_or_404(User, id=cashier_id)
        cashier.delete()
    return redirect('/products/dashboard/?tab=cashiers')


# ================= 5. SUPPLIER CRUD VIEWS =================
def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if name:
            Supplier.objects.create(name=name, phone=phone, email=email)
    return redirect('/products/dashboard/?tab=suppliers')


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if name:
            supplier.name = name
            supplier.phone = phone
            supplier.email = email
            supplier.save()
    return redirect('/products/dashboard/?tab=suppliers')


def delete_supplier(request, supplier_id):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=supplier_id)
        supplier.delete()
    return redirect('/products/dashboard/?tab=suppliers')


# ================= 6. SIZE CRUD VIEWS =================
def add_size(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ProductSize.objects.create(name=name)
    return redirect('/products/dashboard/?tab=size')


def delete_size(request, size_id):
    if request.method == 'POST':
        size = get_object_or_404(ProductSize, id=size_id)
        size.delete()
    return redirect('/products/dashboard/?tab=size')


def edit_size(request, size_id):
    size = get_object_or_404(ProductSize, id=size_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            size.name = name
            size.save()
    return redirect('/products/dashboard/?tab=size')


# ================= 7. VARIANT CRUD VIEWS =================
def add_variant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        product_id = request.POST.get('product')
        if name and product_id:
            product = get_object_or_404(Product, id=product_id)
            ProductVariant.objects.create(name=name, product=product)
    return redirect('/products/dashboard/?tab=variant')


def delete_variant(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        variant.delete()
    return redirect('/products/dashboard/?tab=variant')


# ================= 8. PURCHASE CRUD VIEWS =================
def add_purchase(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        product_id = request.POST.get('product')
        cashier_id = request.POST.get('cashier')
        quantity = int(request.POST.get('quantity') or 0)
        price = request.POST.get('price') or 0

        if product_id:
            supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
            product = get_object_or_404(Product, id=product_id)
            cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
            total = quantity * Decimal(str(price))
            Purchase.objects.create(
                supplier=supplier,
                product=product,
                cashier=cashier,
                quantity=quantity,
                price=price,
                total=total,
            )
            product.stock += quantity
            product.save()
    return redirect('/products/dashboard/?tab=purchase')


def delete_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase.delete()
    return redirect('/products/dashboard/?tab=purchase')


def edit_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        product_id = request.POST.get('product')
        cashier_id = request.POST.get('cashier')
        quantity = int(request.POST.get('quantity') or 0)
        price = request.POST.get('price') or 0

        if product_id:
            supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
            product = get_object_or_404(Product, id=product_id)
            cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
            total = quantity * Decimal(str(price))
            purchase.supplier = supplier
            purchase.product = product
            purchase.cashier = cashier
            purchase.quantity = quantity
            purchase.price = price
            purchase.total = total
            purchase.save()
            product.stock += quantity
            product.save()
    return redirect('/products/dashboard/?tab=purchase')