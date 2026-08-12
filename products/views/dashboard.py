import json
import base64
from io import BytesIO
from collections import defaultdict
from itertools import combinations, groupby
from operator import itemgetter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Product, Category, Subcategory, Supplier, ProductSize, ProductVariant, CashierProfile, Purchase, ManagedProduct
from sales.models import Sale, SaleItem


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


def admin_dashboard(request, section='dashboard'):
    from django.utils import timezone as _tz
    today = _tz.localtime(_tz.now()).date()

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
    today_sales = today_items.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    today_transactions = today_orders.count()
    low_stock_count = products_list.filter(stock__lt=10).count()

    total_revenue = SaleItem.objects.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    total_expenses = 0
    net_balance = total_revenue - total_expenses

    total_products = products_list.count()
    total_categories = categories.count()
    total_suppliers = suppliers.count()

    total_sales = SaleItem.objects.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
    total_transactions = Sale.objects.count()

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
    current_stock = {prod.name: prod.stock for prod in Product.objects.all()}

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
        total_price=F('price') * F('quantity')
    )

    if product_code_filter:
        matching_products = Product.objects.filter(product_code__icontains=product_code_filter)
        report_items = report_items.filter(product_name__in=[p.name for p in matching_products])
    if barcode_filter:
        matching_products = Product.objects.filter(productvariant__barcode__icontains=barcode_filter)
        report_items = report_items.filter(product_name__in=[p.name for p in matching_products]).distinct()

    total_report_sales = report_items.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0
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
        'best_product_names': json.dumps([item['product_name'] for item in best_selling]),
        'best_product_qtys': json.dumps([item['total_qty'] for item in best_selling]),
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

        'active_tab': section,
        'section': section
    }
    return render(request, 'products/admin_dashboard.html', context)
