
import json
import qrcode
import base64
from io import BytesIO
from decimal import Decimal

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


from .models import Product, Category, Subcategory, Supplier, ProductSize, ProductVariant, CashierProfile, Purchase, ManagedProduct
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
    
    if not code:
        return JsonResponse({
            'success': False, 
            'message': 'ကုဒ် ဗလာဖြစ်နေပါသည်။'
        })
    
    # ၁။ Product.product_code နှင့် exact match စစ်ဆေးခြင်း
    try:
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
        pass
    
    # ၂။ Product.name နှင့် case-insensitive ရှာဖွေခြင်း
    try:
        product = Product.objects.get(name__iexact=code)
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price)
            }
        })
    except Product.DoesNotExist:
        pass
    
    # ၃။ Product.name နှင့် icontains ရှာဖွေခြင်း
    product = Product.objects.filter(name__icontains=code).first()
    if product:
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price)
            }
        })
    
    # ၄။ ProductVariant.barcode နှင့် ရှာ�ှေခြင်း
    try:
        variant = ProductVariant.objects.get(barcode=code)
        product = variant.product
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(variant.selling_price or product.price)
            }
        })
    except ProductVariant.DoesNotExist:
        pass
    
    return JsonResponse({
        'success': False, 
        'message': f'ကုန်ပစ္စည်း [{code}] အား ရှာမတွေ့ပါ။'
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


def _generate_dashboard_charts(product_bundles, best_selling, transaction_counts, bundle_limit=5):
    import warnings
    warnings.filterwarnings('ignore', message='Glyph.*missing from font')
    
    sns.set_theme(style="whitegrid")
    
    myanmar_font_path = '/usr/share/fonts/truetype/noto/NotoSansMyanmar-Regular.ttf'
    matplotlib.font_manager.fontManager.addfont(myanmar_font_path)
    plt.rcParams['font.family'] = ['Noto Sans Myanmar', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))

    bundle_names = [b['name'] for b in product_bundles[:bundle_limit]]
    bundle_confidence = [b['confidence'] for b in product_bundles[:bundle_limit]]

    if bundle_names:
        colors_bundle = ['#1F4E79', '#2E75B6', '#007bff', '#3395ff', '#5cadff']
        bars1 = axes[0].barh(bundle_names, bundle_confidence, color=colors_bundle[:len(bundle_names)], height=0.45)
        axes[0].set_xlim(0, 100)
        axes[0].set_xlabel("Confidence (%)", fontsize=10, fontweight='bold')
        axes[0].set_title("ထိပ်တန်းကုန်ပစ္စည်း တွဲဖက်မှုများ\n(Top Product Bundles)", fontsize=12, fontweight='bold', pad=10)
        axes[0].tick_params(axis='both', which='major', labelsize=9)
        for bar in bars1:
            width = bar.get_width()
            axes[0].text(width - 5, bar.get_y() + bar.get_height()/2, f'{width}%',
                         va='center', ha='center', color='white', fontweight='bold', fontsize=9)

    best_product_names = [item['product_name'] for item in best_selling[:8]]
    best_product_qtys = [item['total_qty'] for item in best_selling[:8]]

    if best_product_names:
        bars2 = axes[1].bar(best_product_names, best_product_qtys, color='#1F4E79', width=0.55)
        max_qty = max(best_product_qtys) if best_product_qtys else 1
        axes[1].set_ylim(0, max_qty * 1.2)
        axes[1].set_ylabel("Units Sold", fontsize=10, fontweight='bold')
        axes[1].set_title("Best Selling Products", fontsize=12, fontweight='bold', pad=10)
        axes[1].tick_params(axis='x', rotation=15)
        for bar in bars2:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2, height + max_qty*0.02, f'{height}',
                         va='bottom', ha='center', color='#333333', fontweight='bold', fontsize=9)

    transaction_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    bars3 = axes[2].bar(transaction_days, transaction_counts, color='#8B0000', width=0.55)
    max_count = max(transaction_counts) if max(transaction_counts) > 0 else 1
    axes[2].set_ylim(0, max_count * 1.2)
    axes[2].set_ylabel("Transactions", fontsize=10, fontweight='bold')
    axes[2].set_title("အရောင်းရဆုံး ရက်သတ်တစ်ပတ်\n(Top Sales Days)", fontsize=12, fontweight='bold', pad=10)
    axes[2].tick_params(axis='x', rotation=15)
    for bar in bars3:
        height = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2, height + max_count*0.02, f'{int(height)}',
                     va='bottom', ha='center', color='#333333', fontweight='bold', fontsize=9)

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return image_base64


def admin_dashboard(request):
    from django.utils import timezone as _tz
    today = _tz.localtime(_tz.now()).date()

    from sales.models import Sale, SaleItem

    products_list = Product.objects.all().select_related('category', 'subcategory', 'supplier').prefetch_related('productvariant_set__size')
    products_paginator = Paginator(products_list, 4)
    products_page = products_paginator.get_page(request.GET.get('product_page'))
    _prod_total_pages = products_paginator.num_pages
    _prod_start = products_page.number
    if _prod_start > _prod_total_pages - 1:
        _prod_start = max(1, _prod_total_pages - 1)
    product_page_range = range(_prod_start, min(_prod_start + 1, _prod_total_pages) + 1)

    managed_products = ManagedProduct.objects.all().select_related('category', 'subcategory', 'supplier')
    managed_products_by_name = {mp.name: mp for mp in managed_products}
    for prod in products_page:
        mp = managed_products_by_name.get(prod.name)
        prod.mg = mp
        prod.mg_supplier_name = mp.supplier.name if mp and mp.supplier_id else (prod.supplier.name if prod.supplier_id else '-')
        prod.mg_category_name = mp.category.name if mp and mp.category_id else (prod.category.name if prod.category_id else '-')
        prod.mg_subcategory_name = mp.subcategory.name if mp and mp.subcategory_id else (prod.subcategory.name if prod.subcategory_id else '-')

    categories = Category.objects.all()
    cashiers_list = User.objects.filter(is_superuser=False).select_related('cashier_profile')
    suppliers = Supplier.objects.all()
    sizes = ProductSize.objects.all()
    variants = ProductVariant.objects.all().select_related('product', 'product__category', 'product__subcategory', 'product__supplier', 'size')
    subcategories = Subcategory.objects.all()

    today_orders = Sale.objects.filter(created_at__date=today)
    today_items = SaleItem.objects.filter(sale__in=today_orders)
    today_sales = today_items.aggregate(total=models.Sum(models.F('quantity') * models.F('price')))['total'] or 0
    today_transactions = today_orders.count()
    low_stock_count = products_list.filter(stock__lt=10).count()

    total_revenue = SaleItem.objects.aggregate(total=models.Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_expenses = 0
    net_balance = total_revenue - total_expenses

    total_products = products_list.count()
    total_categories = categories.count()
    total_suppliers = suppliers.count()

    total_sales = SaleItem.objects.aggregate(total=models.Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_transactions = Sale.objects.count()

    from collections import defaultdict
    import json

    all_sale_items = SaleItem.objects.all().select_related('sale')
    sales_by_date = defaultdict(int)
    for item in all_sale_items:
        date_str = item.sale.created_at.strftime('%Y-%m-%d')
        sales_by_date[date_str] += float(item.price * item.quantity)
    sales_dates = sorted(sales_by_date.keys())[-30:]
    sales_values = [sales_by_date[d] for d in sales_dates]

    best_selling = all_sale_items.values('product_name').annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:10]
    best_product_names = [item['product_name'] for item in best_selling]
    best_product_qtys = [item['total_qty'] for item in best_selling]

    transaction_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    transaction_counts = [0] * 7
    for sale in Sale.objects.all():
        day_idx = sale.created_at.weekday()
        transaction_counts[day_idx] += 1

    category_confidence = []
    for cat in Category.objects.all():
        total = ManagedProduct.objects.filter(category=cat).count()
        with_sub = ManagedProduct.objects.filter(category=cat, subcategory__isnull=False).count()
        confidence = round((with_sub / total * 100), 1) if total > 0 else 0
        if total > 0:
            category_confidence.append({
                'name': cat.name,
                'confidence': confidence,
                'total': total,
                'with_sub': with_sub
            })

    from collections import defaultdict
    from itertools import combinations

    sale_items_by_sale = defaultdict(list)
    for item in SaleItem.objects.all().select_related('sale'):
        sale_items_by_sale[item.sale_id].append(item.product_name)

    pair_counts = defaultdict(int)
    product_order_counts = defaultdict(int)

    for sale_id, items in sale_items_by_sale.items():
        unique_products = sorted(set(items))
        for p in unique_products:
            product_order_counts[p] += 1
        for pair in combinations(unique_products, 2):
            pair_counts[pair] += 1

    product_bundles = []
    for pair, count in pair_counts.items():
        prod1, prod2 = pair
        conf1 = round((count / product_order_counts[prod1]) * 100, 1) if product_order_counts[prod1] > 0 else 0
        conf2 = round((count / product_order_counts[prod2]) * 100, 1) if product_order_counts[prod2] > 0 else 0
        confidence = max(conf1, conf2)
        product_bundles.append({
            'name': f"{prod1} & {prod2}",
            'confidence': confidence,
            'count': count,
            'prod1': prod1,
            'prod2': prod2
        })

    product_bundles.sort(key=lambda x: x['confidence'], reverse=True)

    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')[:10]

    purchase_orders = Purchase.objects.all().order_by('-created_at')
    purchased_product_names = Purchase.objects.values_list('product_name', flat=True).distinct().order_by('product_name')
    purchased_products = Product.objects.filter(name__in=purchased_product_names).order_by('name')

    purchase_paginator = Paginator(purchase_orders, 4)
    purchase_page = purchase_paginator.get_page(request.GET.get('purchase_page'))
    _pur_total_pages = purchase_paginator.num_pages
    _pur_start = purchase_page.number
    if _pur_start > _pur_total_pages - 1:
        _pur_start = max(1, _pur_total_pages - 1)
    purchase_page_range = range(_pur_start, min(_pur_start + 1, _pur_total_pages) + 1)

    balance_entries = []
    managed_products_by_name = {mp.name: mp for mp in ManagedProduct.objects.all()}

    current_stock = {}
    for prod in Product.objects.all():
        current_stock[prod.name] = prod.stock

    for p in Purchase.objects.all().select_related('cashier'):
        product_name = p.product_name
        product = Product.objects.filter(name=product_name).first()
        mp = managed_products_by_name.get(product_name)
        
        if product:
            subcategory = product.subcategory.name if product.subcategory_id else (mp.subcategory.name if mp and mp.subcategory_id else (product.category.name if product.category_id else '-'))
        elif mp:
            subcategory = mp.subcategory.name if mp.subcategory_id else (mp.category.name if mp.category_id else '-')
        else:
            subcategory = '-'
            
        balance_entries.append({
            'id': p.id,
            'product_name': product_name,
            'group_key': product_name,
            'subcategory': subcategory,
            'cashier': p.cashier.username if p.cashier else '-',
            'type': 'Purchase',
            'purchase_qty': p.quantity,
            'sale_qty': 0,
            'stock': current_stock.get(product_name, 0),
            'date': p.created_at,
        })

    for item in SaleItem.objects.all().select_related('sale__cashier'):
        raw_product_name = item.product_name
        product_name = raw_product_name
        if '(' in product_name:
            product_name = product_name.split('(')[0].strip()
        
        product = Product.objects.filter(name=product_name).first()
        mp = managed_products_by_name.get(product_name)
        
        if product:
            subcategory = product.subcategory.name if product.subcategory_id else (mp.subcategory.name if mp and mp.subcategory_id else (product.category.name if product.category_id else '-'))
        elif mp:
            subcategory = mp.subcategory.name if mp.subcategory_id else (mp.category.name if mp.category_id else '-')
        else:
            subcategory = '-'
            
        balance_entries.append({
            'id': item.sale.id,
            'product_name': raw_product_name,
            'group_key': product_name,
            'subcategory': subcategory,
            'cashier': item.sale.cashier.username if item.sale.cashier else '-',
            'type': 'Sale',
            'purchase_qty': 0,
            'sale_qty': item.quantity,
            'stock': current_stock.get(product_name, 0),
            'date': item.sale.created_at,
        })

    from itertools import groupby
    from operator import itemgetter

    balance_entries.sort(key=lambda x: (x['product_name'], x['date']))

    for key, group in groupby(balance_entries, key=itemgetter('group_key')):
        entries = list(group)
        
        current_bal = current_stock.get(key, 0)
        
        for entry in entries:
            if entry['type'] == 'Purchase':
                current_bal += entry['purchase_qty']
            else:
                current_bal -= entry['sale_qty']
            entry['balance'] = current_bal

    balance_entries.sort(key=lambda x: x['date'], reverse=True)

    balance_paginator = Paginator(balance_entries, 10)
    balance_page = balance_paginator.get_page(request.GET.get('balance_page'))
    _bal_total_pages = balance_paginator.num_pages
    _bal_start = balance_page.number
    if _bal_start > _bal_total_pages - 1:
        _bal_start = max(1, _bal_total_pages - 1)
    balance_page_range = range(_bal_start, min(_bal_start + 1, _bal_total_pages) + 1)

    start_date = request.GET.get('start_date', '')
    search_month = request.GET.get('search_month', '')
    search_year = request.GET.get('search_year', '')
    cashier_filter = request.GET.get('cashier_filter', 'all')
    product_filter = request.GET.get('product_filter', 'all')
    today_sales_filter = request.GET.get('today_sales', '')
    product_code_filter = request.GET.get('product_code', '')
    barcode_filter = request.GET.get('barcode', '')

    report_orders = Sale.objects.all()

    if today_sales_filter == '1':
        report_orders = report_orders.filter(created_at__date=today)
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

    report_items = SaleItem.objects.filter(sale__in=report_orders).select_related('sale', 'sale__cashier').annotate(
        total_price=models.F('price') * models.F('quantity')
    )
    
    if product_code_filter:
        matching_products = Product.objects.filter(product_code__icontains=product_code_filter)
        report_items = report_items.filter(product_name__in=[p.name for p in matching_products])
    if barcode_filter:
        matching_products = Product.objects.filter(productvariant__barcode__icontains=barcode_filter)
        report_items = report_items.filter(product_name__in=[p.name for p in matching_products]).distinct()

    total_report_sales = report_items.aggregate(total=Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_report_trans = report_items.values('sale').distinct().count()

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

    management_paginator = Paginator(ManagedProduct.objects.all().order_by('id'), 4)
    management_page = management_paginator.get_page(request.GET.get('management_page'))
    _mgmt_total_pages = management_paginator.num_pages
    _mgmt_start = management_page.number
    if _mgmt_start > _mgmt_total_pages - 1:
        _mgmt_start = max(1, _mgmt_total_pages - 1)
    management_page_range = range(_mgmt_start, min(_mgmt_start + 1, _mgmt_total_pages) + 1)

    variant_paginator = Paginator(variants, 4)
    variant_page = variant_paginator.get_page(request.GET.get('variant_page'))
    _var_total_pages = variant_paginator.num_pages
    _var_start = variant_page.number
    if _var_start > _var_total_pages - 1:
        _var_start = max(1, _var_total_pages - 1)
    variant_page_range = range(_var_start, min(_var_start + 1, _var_total_pages) + 1)

    see_all_bundles = request.GET.get('see_all_bundles') == '1'
    bundle_limit = len(product_bundles) if see_all_bundles else 5
    dashboard_chart = _generate_dashboard_charts(product_bundles, best_selling, transaction_counts, bundle_limit=bundle_limit)

    context = {
        'products': products_page,
        'product_page': products_page,
        'product_page_range': product_page_range,
        'management_page': management_page,
        'management_page_range': management_page_range,
        'categories': categories,
        'cashiers': cashiers_list,
        'suppliers': suppliers,
        'sizes': sizes,
        'size_page': size_page,
        'size_page_range': size_page_range,
        'variants': variants,
        'variant_page': variant_page,
        'variant_page_range': variant_page_range,
        'subcategories': subcategories,
        'subcategory_page': subcategory_page,
        'subcategory_page_range': subcategory_page_range,

        'today_sales': today_sales,
        'today_transactions': today_transactions,
        'low_stock_count': low_stock_count,
        'total_sales': total_sales,
        'total_transactions': total_transactions,

        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_balance': net_balance,

        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'dashboard_chart': dashboard_chart,
        'see_all_bundles': see_all_bundles,
        'product_bundles': product_bundles,
        
        'sales_dates': json.dumps(sales_dates),
        'sales_values': json.dumps(sales_values),
        'best_product_names': json.dumps(best_product_names),
        'best_product_qtys': json.dumps(best_product_qtys),
        'transaction_days': json.dumps(transaction_days),
        'transaction_counts': json.dumps(transaction_counts),
        'category_confidence': category_confidence,
        'low_stock_products': low_stock_products,
        
        'purchase_orders': purchase_orders,
        'purchased_product_names': purchased_product_names,
        'purchased_products': purchased_products,
        'purchase_page': purchase_page,
        'purchase_page_range': purchase_page_range,
        'balance_entries': balance_page,
        'balance_page': balance_page,
        'balance_page_range': balance_page_range,
        
        'report_items': report_items,
        'total_report_sales': total_report_sales,
        'total_report_trans': total_report_trans,
        
        'start_date': start_date,
        'search_month': search_month,
        'search_year': search_year,
        'cashier_filter': cashier_filter,
        'product_filter': product_filter,
        'today_sales_filter': today_sales_filter,
        'product_code_filter': product_code_filter,
        'barcode_filter': barcode_filter,
        
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
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        supplier_id = request.POST.get('supplier')

        product = Product(
            name=p_name,
            price=price,
            stock=stock,
            category_id=category_id,
            subcategory_id=subcategory_id if subcategory_id else None,
            supplier_id=supplier_id if supplier_id else None,
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
        return redirect('/products/dashboard/?tab=management')

    return redirect('/products/dashboard/?tab=management')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.product_code = request.POST.get('product_code')
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')

        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        supplier_id = request.POST.get('supplier')

        product.category = get_object_or_404(Category, id=category_id)
        product.subcategory = get_object_or_404(Subcategory, id=subcategory_id) if subcategory_id else None
        product.supplier = get_object_or_404(Supplier, id=supplier_id) if supplier_id else None

        product.save()
        return redirect('/products/dashboard/?tab=management')
    return redirect('/products/dashboard/?tab=management')

def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
    return redirect('/products/dashboard/?tab=products')


# ================= 2.5. MANAGED PRODUCT CRUD VIEWS =================
def add_managed_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        supplier_id = request.POST.get('supplier')
        if name and category_id:
            category = get_object_or_404(Category, id=category_id)
            subcategory = get_object_or_404(Subcategory, id=subcategory_id) if subcategory_id else None
            supplier = get_object_or_404(Supplier, id=supplier_id) if supplier_id else None
            ManagedProduct.objects.create(
                name=name,
                category=category,
                subcategory=subcategory,
                supplier=supplier,
            )
    return redirect('/products/dashboard/?tab=management')


def edit_managed_product(request, managed_product_id):
    managed_product = get_object_or_404(ManagedProduct, id=managed_product_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        supplier_id = request.POST.get('supplier')
        if name and category_id:
            managed_product.name = name
            managed_product.category = get_object_or_404(Category, id=category_id)
            managed_product.subcategory = get_object_or_404(Subcategory, id=subcategory_id) if subcategory_id else None
            managed_product.supplier = get_object_or_404(Supplier, id=supplier_id) if supplier_id else None
            managed_product.save()
    return redirect('/products/dashboard/?tab=management')


def delete_managed_product(request, managed_product_id):
    if request.method == 'POST':
        managed_product = get_object_or_404(ManagedProduct, id=managed_product_id)
        managed_product.delete()
    return redirect('/products/dashboard/?tab=management')


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
def _get_or_create_product_by_name(product_name):
    category, _ = Category.objects.get_or_create(name='Uncategorized')
    product_code = f"PUR_{abs(hash(product_name)) % 100000:05d}"
    product, _ = Product.objects.get_or_create(
        name=product_name,
        defaults={
            'product_code': product_code,
            'price': 0,
            'stock': 0,
            'category': category,
            'subcategory': None,
            'supplier': None,
        }
    )
    return product


def add_variant(request):
    if request.method == 'POST':
        product_name = request.POST.get('product', '').strip()
        size_id = request.POST.get('size')
        buying_price = request.POST.get('buying_price') or 0
        selling_price = request.POST.get('selling_price') or 0
        exp = request.POST.get('exp', '')
        qty = request.POST.get('qty') or 0
        barcode = request.POST.get('barcode', '').strip()

        if product_name:
            product = _get_or_create_product_by_name(product_name)
            size = get_object_or_404(ProductSize, id=size_id) if size_id else None
            variant = ProductVariant.objects.create(
                name=barcode or product_name,
                product=product,
                size=size,
                buying_price=buying_price,
                selling_price=selling_price,
                exp=exp,
                qty=qty,
                barcode=barcode,
            )
            if barcode and not variant.qr_code:
                import qrcode
                from io import BytesIO
                from django.core.files import File
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(barcode)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                variant.qr_code.save(f"qr_{barcode}.png", File(buffer), save=False)
                variant.save()
    return redirect('/products/dashboard/?tab=variant')


def edit_variant(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if request.method == 'POST':
        product_name = request.POST.get('product', '').strip()
        size_id = request.POST.get('size')
        variant.buying_price = request.POST.get('buying_price') or 0
        variant.selling_price = request.POST.get('selling_price') or 0
        variant.exp = request.POST.get('exp', '')
        variant.qty = request.POST.get('qty') or 0
        variant.barcode = request.POST.get('barcode', '').strip()

        if product_name:
            variant.product = _get_or_create_product_by_name(product_name)
        variant.size = get_object_or_404(ProductSize, id=size_id) if size_id else None

        if variant.barcode and not variant.qr_code:
            import qrcode
            from io import BytesIO
            from django.core.files import File
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(variant.barcode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            variant.qr_code.save(f"qr_{variant.barcode}.png", File(buffer), save=False)

        variant.save()
    return redirect('/products/dashboard/?tab=variant')


def delete_variant(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        variant.delete()
    return redirect('/products/dashboard/?tab=variant')


# ================= 8. PURCHASE CRUD VIEWS =================
def _get_or_create_uncategorized():
    cat, _ = Category.objects.get_or_create(name="Uncategorized")
    return cat


def add_purchase(request):
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        product_name = request.POST.get('product_name', '').strip()
        cashier_id = request.POST.get('cashier')
        quantity = int(request.POST.get('quantity') or 0)
        price = request.POST.get('price') or 0

        supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
        cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
        total = quantity * Decimal(str(price))
        Purchase.objects.create(
            supplier=supplier,
            product_name=product_name,
            cashier=cashier,
            quantity=quantity,
            price=price,
            total=total,
        )
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
        product_name = request.POST.get('product_name', '').strip()
        cashier_id = request.POST.get('cashier')
        quantity = int(request.POST.get('quantity') or 0)
        price = request.POST.get('price') or 0

        supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
        cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
        total = quantity * Decimal(str(price))
        purchase.supplier = supplier
        purchase.product_name = product_name
        purchase.cashier = cashier
        purchase.quantity = quantity
        purchase.price = price
        purchase.total = total
        purchase.save()
    return redirect('/products/dashboard/?tab=purchase')