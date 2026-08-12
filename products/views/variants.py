import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File

from ..models import Product, Category, ProductSize, ProductVariant
from .dashboard import admin_dashboard


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


def add_size(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ProductSize.objects.create(name=name)
    return admin_dashboard(request, section='size')


def delete_size(request, size_id):
    if request.method == 'POST':
        size = get_object_or_404(ProductSize, id=size_id)
        size.delete()
    return admin_dashboard(request, section='size')


def edit_size(request, size_id):
    size = get_object_or_404(ProductSize, id=size_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            size.name = name
            size.save()
    return admin_dashboard(request, section='size')


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
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(barcode)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                variant.qr_code.save(f"qr_{barcode}.png", File(buffer), save=False)
                variant.save()
    return admin_dashboard(request, section='variant')


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
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(variant.barcode)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            variant.qr_code.save(f"qr_{variant.barcode}.png", File(buffer), save=False)

        variant.save()
    return admin_dashboard(request, section='variant')


def delete_variant(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        variant.delete()
    return admin_dashboard(request, section='variant')
