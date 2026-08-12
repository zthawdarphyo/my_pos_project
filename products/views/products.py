import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
from django.conf import settings
from django.db import models

from ..models import Product, Category, Subcategory, Supplier, ManagedProduct
from .dashboard import admin_dashboard


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
        product.save()
    return admin_dashboard(request, section='management')


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
    return admin_dashboard(request, section='management')


def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
    return admin_dashboard(request, section='products')


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
    return admin_dashboard(request, section='management')


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
    return admin_dashboard(request, section='management')


def delete_managed_product(request, managed_product_id):
    if request.method == 'POST':
        managed_product = get_object_or_404(ManagedProduct, id=managed_product_id)
        managed_product.delete()
    return admin_dashboard(request, section='management')
