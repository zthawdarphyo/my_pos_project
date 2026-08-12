from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F

from ..models import Purchase, Category, Product
from .dashboard import admin_dashboard


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

        supplier = Purchase._meta.get_field('supplier').related_model.objects.filter(id=supplier_id).first() if supplier_id else None
        from django.contrib.auth.models import User
        cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
        total = quantity * float(price)
        Purchase.objects.create(
            supplier=supplier,
            product_name=product_name,
            cashier=cashier,
            quantity=quantity,
            price=price,
            total=total,
        )
    return admin_dashboard(request, section='purchase')


def delete_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase.delete()
    return admin_dashboard(request, section='purchase')


def edit_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        product_name = request.POST.get('product_name', '').strip()
        cashier_id = request.POST.get('cashier')
        quantity = int(request.POST.get('quantity') or 0)
        price = request.POST.get('price') or 0

        from django.contrib.auth.models import User
        supplier = Purchase._meta.get_field('supplier').related_model.objects.filter(id=supplier_id).first() if supplier_id else None
        cashier = User.objects.filter(id=cashier_id).first() if cashier_id else None
        total = quantity * float(price)
        purchase.supplier = supplier
        purchase.product_name = product_name
        purchase.cashier = cashier
        purchase.quantity = quantity
        purchase.price = price
        purchase.total = total
        purchase.save()
    return admin_dashboard(request, section='purchase')
