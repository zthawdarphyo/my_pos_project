from django.shortcuts import render, redirect, get_object_or_404

from ..models import Supplier
from .dashboard import admin_dashboard


def add_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if name:
            Supplier.objects.create(name=name, phone=phone, email=email)
    return admin_dashboard(request, section='suppliers')


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
    return admin_dashboard(request, section='suppliers')


def delete_supplier(request, supplier_id):
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, id=supplier_id)
        supplier.delete()
    return admin_dashboard(request, section='suppliers')
