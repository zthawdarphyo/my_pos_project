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
    """ Save Invoice + ပိုင်းချမ်းသောရုပ်ပုံ (PNG) များကို သိမ်းဆည်းမည့် API """
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])
        
        subtotal = sum(float(item['price']) * item['qty'] for item in items)
        tax = subtotal * TAX_RATE
        
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
        
        invoice_num = f"SALE-{sale.id}"
        img_dir = os.path.join(settings.MEDIA_ROOT, 'invoices_images')
        os.makedirs(img_dir, exist_ok=True)
        img_path = os.path.join(img_dir, f"{invoice_num}.png")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (600, 800), color='white')
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            draw.text((50, 20), "CITY MART STYLE PYTHON POS", fill='black', font=font)
            draw.text((50, 50), f"Sale ID: {invoice_num}", fill='black', font=font)
            draw.text((50, 75), f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font_small)
            draw.line([(50, 100), (550, 100)], fill='black', width=1)
            
            y_pos = 120
            for item in items:
                draw.text((50, y_pos), f"{item['name']} x {item['qty']} = {float(item['price']) * item['qty']} MMK", fill='black', font=font_small)
                y_pos += 25
            
            y_pos += 10
            draw.line([(50, y_pos), (550, y_pos)], fill='black', width=1)
            y_pos += 10
            draw.text((50, y_pos), f"Subtotal: {subtotal} MMK", fill='black', font=font_small)
            y_pos += 20
            draw.text((50, y_pos), f"Tax (5%): {tax} MMK", fill='black', font=font_small)
            y_pos += 20
            draw.text((50, y_pos), f"Grand Total: {subtotal + tax} MMK", fill='black', font=font)
            
            img.save(img_path, 'PNG')
            sale.image_file = f"invoices_images/{invoice_num}.png"
            sale.save()
        except Exception as e:
            print(f"Image save error: {e}")
        
        return JsonResponse({'success': True, 'sale_id': sale.id})
    return JsonResponse({'success': False})

def scan_product_api(request):
    code = request.GET.get('code', '').strip()
    try:
        
        product = Product.objects.get(product_code=code) 
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
            product = Product.objects.get(product_code=barcode_id)
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
        product = Product.objects.filter(product_code=manual_code).first()
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

def invoice_list(request):
    orders = Order.objects.all().order_by('-created_at')
    sales = Sale.objects.all().order_by('-created_at')
    return render(request, 'sales/invoice_list.html', {'orders': orders, 'sales': sales})

def invoice_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'sales/invoice.html', {'order': order})

def sale_invoice(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/invoice.html', {'sale': sale})

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
        product = Product.objects.get(product_code=barcode_id)
        OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=item['price'])
        product.stock -= item['quantity']  
        product.save()

    
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'invoices_pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"{invoice_num}.pdf")
    img_path = os.path.join(pdf_dir, f"{invoice_num}.png")
    
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
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (600, 800), color='white')
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        draw.text((50, 20), "CITY MART STYLE PYTHON POS", fill='black', font=font)
        draw.text((50, 50), f"Invoice: {invoice_num}", fill='black', font=font)
        draw.text((50, 75), f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='black', font=font_small)
        draw.line([(50, 100), (550, 100)], fill='black', width=1)
        
        y_pos = 120
        for barcode_id, item in cart.items():
            draw.text((50, y_pos), f"{item['name']} x {item['quantity']} = {item['price'] * item['quantity']} MMK", fill='black', font=font_small)
            y_pos += 25
        
        y_pos += 10
        draw.line([(50, y_pos), (550, y_pos)], fill='black', width=1)
        y_pos += 10
        draw.text((50, y_pos), f"Subtotal: {subtotal} MMK", fill='black', font=font_small)
        y_pos += 20
        draw.text((50, y_pos), f"Tax (5%): {tax} MMK", fill='black', font=font_small)
        y_pos += 20
        draw.text((50, y_pos), f"Grand Total: {total} MMK", fill='black', font=font)
        
        img.save(img_path, 'PNG')
    except Exception as e:
        print(f"Image save error: {e}")
    
    order.pdf_file = f"invoices_pdf/{invoice_num}.pdf"
    order.save()
    
    request.session['cart'] = {}
    return render(request, 'sales/invoice.html', {'order': order})