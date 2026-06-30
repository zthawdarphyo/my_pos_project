
import json
import qrcode
from io import BytesIO

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


from django.core.files import File


from .models import Product, Category
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
    # အခြေခံ Queryset များကို ဆွဲထုတ်ခြင်း (Cashier အတွက် superuser မဟုတ်သူများကို ယူထားသည်)
    products_list = Product.objects.all()
    categories = Category.objects.all()
    cashiers_list = User.objects.filter(is_superuser=False)

    # UI Form ဘက်ကနေ ပို့လိုက်မယ့် Filter တန်ဖိုးများကို လက်ခံခြင်း
    start_date = request.GET.get('start_date', '')
    # end_date = request.GET.get('end_date', '')
    search_month = request.GET.get('search_month', '')  # HTML output format: 'YYYY-MM'
    search_year = request.GET.get('search_year', '')    # Text input format: 'YYYY'
    cashier_filter = request.GET.get('cashier_filter', 'all')
    product_filter = request.GET.get('product_filter', 'all')

    # အခြေခံ Order Query (အစကနဦးတွင် အားလုံးပြရန်)
    report_orders = Order.objects.all()

    # ၁။ ပြက္ခဒိန် ရက်စွဲအကန့်အသတ် (ထည့်သွင်းထားမှသာ စစ်ထုတ်မည်)
    if start_date:
        report_orders = report_orders.filter(created_at__date__gte=start_date)
    # if end_date:
    #     report_orders = report_orders.filter(created_at__date__lte=end_date)

    # ၂။ လအလိုက် သီးသန့်ရွေးချယ်ရှာဖွေခြင်း (ဥပမာ - ၂၀၂၆ ခုနှစ် ၀၆ လ)
    if search_month:
        try:
            year, month = search_month.split('-')
            report_orders = report_orders.filter(created_at__year=year, created_at__month=month)
        except ValueError:
            pass

    # ၃။ နှစ်အလိုက် သီးသန့်ရိုက်ရှာခြင်း (ဥပမာ - ၂၀၂၆)
    if search_year:
        report_orders = report_orders.filter(created_at__year=search_year)

    # ၄။ မည်သည့် Cashier ရောင်းချခဲ့သနည်းဟု စစ်ထုတ်ခြင်း
    if cashier_filter != 'all':
        report_orders = report_orders.filter(cashier_id=cashier_filter)

    # Order တွေ စစ်ထုတ်ပြီးပြီဖြစ်လို့ ရောင်းချခဲ့ရတဲ့ Items (ပစ္စည်းများ) ကို ဆွဲထုတ်ခြင်း
    # Database Query မြန်ဆန်စေရန် select_related သုံးထားပါသည်
    report_items = OrderItem.objects.filter(order__in=report_orders).select_related('product', 'order', 'order__cashier')

    # ၅။ မည်သည့် Product ကို ရောင်းချခဲ့သနည်းဟု ထပ်မံစစ်ထုတ်ခြင်း
    if product_filter != 'all':
        report_items = report_items.filter(product_id=product_filter)

    # စစ်ထုတ်ထားသော အရောင်းစာရင်းမှ စုစုပေါင်း အရောင်းပမာဏကို တွက်ချက်ခြင်း
    total_report_sales = report_items.aggregate(total=Sum(models.F('quantity') * models.F('price')))['total'] or 0
    total_report_trans = report_items.values('order').distinct().count()

    context = {
        'products': products_list,
        'categories': categories,
        'cashiers': cashiers_list,
        
        # စစ်ထုတ်ပြီး ထွက်လာသော အရောင်းမှတ်တမ်းဒေတာများ
        'report_items': report_items,
        'total_report_sales': total_report_sales,
        'total_report_trans': total_report_trans,
        
        # အသုံးပြုသူ ရွေးချယ်ခဲ့သည်များကို UI တွင် Select Box ၌ ပြန်လည်ပြသပေးရန်
        'start_date': start_date,
        # 'end_date': end_date,
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

        # Model ထဲက Field နာမည်အမှန်များဖြစ်သည့် name နှင့် stock ကို သုံးထားပါသည်
        product = Product(
            name=p_name,
            price=price,
            stock=stock,
            category_id=category
        )

        # အပြင်က QR/Barcode ပါပြီးသားဆိုလျှင်
        if p_code:
            product.product_code = p_code

        # ပစ္စည်းမှာ QR မပါလို့ ကိုယ်တိုင် ထုတ်ပေးရလျှင်
        else:
            generated_code = f"POS-{uuid.uuid4().hex[:8].upper()}" 
            product.product_code = generated_code
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(generated_code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            # (သတိပြုရန်) သင့် Model ထဲတွင် qr_image သို့မဟုတ် qr_code အဆင်ပြေရာ သုံးနိုင်သည်
            # လက်ရှိ Traceback အရ Field အမည်မှာ qr_code ဟု တွေ့ရသဖြင့် အောက်ပါအတိုင်း ပြောင်းထားပါသည်
            if hasattr(product, 'qr_code'):
                product.qr_code.save(f"{generated_code}.png", File(buffer), save=False)
            elif hasattr(product, 'qr_image'):
                product.qr_image.save(f"{generated_code}.png", File(buffer), save=False)

        # Database ထဲသို့ သိမ်းဆည်းခြင်း
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


# ================= 4. CASHIER CRUD VIEWS =================
def add_cashier(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True  # POS စနစ်သုံးနိုင်ရန် Staff Access ပေးထားခြင်း
            user.save()
    return redirect('/products/dashboard/?tab=cashiers')


def delete_cashier(request, cashier_id):
    if request.method == 'POST':
        cashier = get_object_or_404(User, id=cashier_id)
        cashier.delete()
    return redirect('/products/dashboard/?tab=cashiers')