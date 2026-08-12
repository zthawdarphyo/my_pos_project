import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from ..models import Product, ProductVariant


@csrf_exempt
def save_transaction(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get('cart', [])
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        return JsonResponse({'success': True})


def cashier_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('products:admin_dashboard')
        else:
            return redirect('products:pos_page')

    if request.method == "POST":
        user_input = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=user_input, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('products:admin_dashboard')
            else:
                return redirect('products:pos_page')
        else:
            return render(request, 'products/cashier_pos.html', {'error': True})
    return render(request, 'products/cashier_pos.html')


def pos_page(request):
    return render(request, 'products/pos_invoice.html')


def scan_product_api(request, product_code):
    code = product_code.strip()
    if not code:
        return JsonResponse({'success': False, 'message': 'ကုဒ် ဗလာဖြစ်နေပါသည်။'})

    try:
        product = Product.objects.get(product_code=code)
        return JsonResponse({
            'success': True,
            'product': {'id': product.id, 'name': product.name, 'price': float(product.price)}
        })
    except Product.DoesNotExist:
        pass

    try:
        product = Product.objects.get(name__iexact=code)
        return JsonResponse({
            'success': True,
            'product': {'id': product.id, 'name': product.name, 'price': float(product.price)}
        })
    except Product.DoesNotExist:
        pass

    product = Product.objects.filter(name__icontains=code).first()
    if product:
        return JsonResponse({
            'success': True,
            'product': {'id': product.id, 'name': product.name, 'price': float(product.price)}
        })

    try:
        variant = ProductVariant.objects.get(barcode=code)
        product = variant.product
        return JsonResponse({
            'success': True,
            'product': {'id': product.id, 'name': product.name, 'price': float(variant.selling_price or product.price)}
        })
    except ProductVariant.DoesNotExist:
        pass

    return JsonResponse({'success': False, 'message': f'ကုန်ပစ္စည်း [{code}] အား ရှာမတွေ့ပါ။'})


LATEST_SCAN_CODE = None


def get_scanned_code(request):
    global LATEST_SCAN_CODE
    if LATEST_SCAN_CODE:
        temp_code = LATEST_SCAN_CODE
        LATEST_SCAN_CODE = None
        return JsonResponse({"code": temp_code})
    return JsonResponse({"code": None})
