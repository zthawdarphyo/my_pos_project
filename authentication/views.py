from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from products.models import Product, Category, Supplier
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

def login_view(request):
    # အကယ်၍ User က login ဝင်ထားပြီးသား ဖြစ်နေပါက
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin_dashboard')  # Admin Dashboard သို့
        return redirect('cashier_pos')          # Cashier POS သို့

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Django User စနစ်ဖြင့် စစ်ဆေးခြင်း (`zin` လား၊ `cashier` လား)
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            auth_login(request, user)
            
            # 🌟 Role အလိုက် သက်ဆိုင်ရာ လမ်းကြောင်းသို့ ပို့ပေးခြင်း
            if user.is_superuser or user.is_staff:
                # Username: zin (Superuser) ဆိုလျှင် Products ထဲက admin_dashboard သို့သွားမည်
                return redirect('admin_dashboard')
            else:
                # Admin မှ ဆောက်ပေးထားသော ရိုးရိုး Cashier အကောင့်ဆိုလျှင် cashier_pos သို့သွားမည်
                return redirect('cashier_pos')
        else:
            # အကောင့်မှားယွင်းပါက ပြန်ပြမည့် error
            return render(request, 'authentication/login.html', {'error': 'အကောင့် သို့မဟုတ် စကားဝှက် မှားယွင်းနေပါသည်။'})
            
    return render(request, 'authentication/login.html')

def logout_view(request):
    auth_logout(request)
    # Logout ထွက်ပြီးလျှင် NEXT-Gen POS Login Page သို့ အမြဲတန်း တိုက်ရိုက်ပြန်ပို့မည်
    return redirect('login')

@login_required
def admin_dashboard(request):
    # Admin မဟုတ်ရင် ဝင်ခွင့်မပြုပါ
    if not request.user.is_superuser:
        return redirect('pos_dashboard')

    # ၉။ Sales Monitoring (Today) & ၁၀။ Reports (ဒီနေရာတွင် Order Model နှင့် ချိတ်ဆက်တွက်ချက်ရန်)
    today = timezone.now().date()
    
    # ဥပမာ ဒေတာများပြသရန် (Order Model အစုံရှိပါက ၎င်းမှ ယူရပါမည်)
    today_sales = 500000  # 500,000 MMK
    today_transactions = 120
    
    # ၁၁။ Low Stock Alert စစ်ထုတ်ခြင်း
    low_stock_products = Product.objects.filter(stock__lte=5)
    
    # စုစုပေါင်း စာရင်းများ
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    all_suppliers = Supplier.objects.all()
    cashiers = User.objects.filter(is_superuser=False)

    context = {
        'today_sales': today_sales,
        'today_transactions': today_transactions,
        'low_stock_products': low_stock_products,
        'all_products': all_products,
        'all_categories': all_categories,
        'all_suppliers': all_suppliers,
        'cashiers': cashiers,
    }
    return render(request, 'authentication/admin_dashboard.html', context)

# ၄။ Stock In & Stock Adjustment Management
@login_required
def adjust_stock(request, product_id):
    if not request.user.is_superuser:
        return redirect('pos_dashboard')
        
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        adjustment_type = request.POST.get('type') # 'add' သို့မဟုတ် 'adjust'
        quantity = int(request.POST.get('quantity', 0))
        
        if adjustment_type == 'add':
            product.stock += quantity # Current Stock + 100 = New Stock
            messages.success(request, f"{product.name} ထဲသို့ Stock +{quantity} ထည့်သွင်းပြီးပါပြီ။")
        elif adjustment_type == 'adjust':
            product.stock = quantity # စိတ်ကြိုက်ပြင်ဆင်ခြင်း
            messages.success(request, f"{product.name} ၏ Stock ကို {quantity} သို့ ပြင်ဆင်ပြီးပါပြီ။")
            
        product.save()
    return redirect('admin_dashboard')

# authentication/views.py ရဲ့ အောက်ဆုံးမှာ ဒါလေး ထည့်ပေးပါ
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('products:admin_dashboard')
                return redirect('pos_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# authentication/views.py ရဲ့ အောက်ဆုံးမှာ ဒါလေး ထပ်ဖြည့်ပေးပါ
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    messages.success(request, "Account ထဲမှ အောင်မြင်စွာ ထွက်ပြီးပါပြီ။")
    return redirect('custom_login') # Logout ဖြစ်ပြီးရင် Login Page ကို ပြန်လွှတ်တာပါ

# authentication/views.py ရဲ့ အောက်ဆုံးမှာ ဒါလေး ထပ်ဖြည့်ပေးပါ

@login_required
def admin_manage_cashiers(request):
    if not request.user.is_superuser:
        return redirect('pos_dashboard')
        
    cashiers = User.objects.filter(is_superuser=False)
    
    context = {
        'cashiers': cashiers,
    }
    # သင့်မှာ template ဖိုင် ရှိပြီးသားဆိုရင် ၎င်းအမည်ကို ပြောင်းပေးပါ (ဥပမာ - manage_cashiers.html)
    return render(request, 'authentication/admin_dashboard.html', context)