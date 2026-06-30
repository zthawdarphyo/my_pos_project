from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from .models import Order, OrderItem
import datetime, os
from django.conf import settings
from reportlab.pdfgen import canvas

TAX_RATE = 0.05 

from django.http import JsonResponse
from .models import Product ,Sale,SaleItem
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_invoice_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        
        
        subtotal = sum(float(item['price']) * item['qty'] for item in items)
        tax = subtotal * 0.05
        
       
        sale = Sale.objects.create(
            cashier=request.user,
            total_amount=subtotal + tax,
            tax=tax
        )
        
        
        for item in items:
            SaleItem.objects.create(
                sale=sale,
                product_name=item['name'],
                quantity=item['qty'],
                price=item['price']
            )
            
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def scan_product_api(request):
    code = request.GET.get('code', '').strip()
    try:
        
        product = Product.objects.get(qr_code=code) 
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price) 
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'ကုန်ပစ္စည်း ရှာမတွေ့ပါ။'})

@csrf_exempt
def add_to_cart_api(request):
    """ Laptop Camera မှ QR ကုဒ်လှမ်းဖတ်လျှင် ဈေးဝယ်ခြင်းထဲသို့ Auto လာထည့်ပေးမည့် API """
    if request.method == 'POST':
        barcode_id = request.POST.get('barcode_id')
        try:
            product = Product.objects.get(barcode_id=barcode_id)
            cart = request.session.get('cart', {})
            if barcode_id in cart:
                cart[barcode_id]['quantity'] += 1
            else:
                cart[barcode_id] = {'name': product.name, 'price': float(product.price), 'quantity': 1}
            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)

def pos_dashboard(request):
    """ Cashier မြင်ရမည့် POS Counter & လက်ဖြင့် ရိုက်ထည့်နိုင်သည့် စနစ် """
    if request.method == 'POST':
        manual_code = request.POST.get('manual_barcode')
        product = Product.objects.filter(barcode_id=manual_code).first()
        if product:
            cart = request.session.get('cart', {})
            if manual_code in cart:
                cart[manual_code]['quantity'] += 1
            else:
                cart[manual_code] = {'name': product.name, 'price': float(product.price), 'quantity': 1}
            request.session['cart'] = cart
            
    cart = request.session.get('cart', {})
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    
    return render(request, 'sales/pos_dashboard.html', {
        'cart': cart, 'subtotal': subtotal, 'tax': tax, 'total': total
    })

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('pos_dashboard')

def checkout(request):
    """ ငွေရှင်းပြီး စနစ်တကျ PDF ဖန်တီးသိမ်းဆည်းမည့်စနစ် """
    cart = request.session.get('cart', {})
    if not cart: return redirect('pos_dashboard')
    
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    invoice_num = f"INV-{int(datetime.datetime.now().timestamp())}"
    
    order = Order.objects.create(
        cashier=request.user, subtotal=subtotal, tax_amount=tax, total_amount=total, invoice_number=invoice_num
    )
    
    for barcode_id, item in cart.items():
        product = Product.objects.get(barcode_id=barcode_id)
        OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=item['price'])
        product.stock_quantity -= item['quantity']  
        product.save()

    
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'invoices_pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"{invoice_num}.pdf")
    
    p = canvas.Canvas(pdf_path)
    p.drawString(100, 800, "CITY MART STYLE PYTHON POS")
    p.drawString(100, 780, f"Invoice: {invoice_num}")
    p.drawString(100, 760, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 740, "--------------------------------------------------")
    
    y = 710
    for barcode_id, item in cart.items():
        p.drawString(100, y, f"{item['name']} x {item['quantity']} = {item['price'] * item['quantity']} MMK")
        y -= 20
        
    p.drawString(100, y-20, f"Subtotal: {subtotal} MMK")
    p.drawString(100, y-40, f"Tax (5%): {tax} MMK")
    p.drawString(100, y-60, f"Grand Total: {total} MMK")
    p.showPage()
    p.save()
    
    order.pdf_file = f"invoices_pdf/{invoice_num}.pdf"
    order.save()
    
    request.session['cart'] = {}
    return render(request, 'sales/invoice.html', {'order': order})