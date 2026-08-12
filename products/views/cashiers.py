from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from ..models import CashierProfile
from .dashboard import admin_dashboard


def add_cashier(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')

        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.save()
            CashierProfile.objects.create(user=user, phone=phone)
    return admin_dashboard(request, section='cashiers')


def edit_cashier(request, cashier_id):
    cashier = get_object_or_404(User, id=cashier_id)
    if request.method == 'POST':
        cashier.username = request.POST.get('username')
        cashier.email = request.POST.get('email')
        phone = request.POST.get('phone', '')

        profile, created = CashierProfile.objects.get_or_create(user=cashier)
        profile.phone = phone
        profile.save()

        cashier.save()
    return admin_dashboard(request, section='cashiers')


def delete_cashier(request, cashier_id):
    if request.method == 'POST':
        cashier = get_object_or_404(User, id=cashier_id)
        cashier.delete()
    return admin_dashboard(request, section='cashiers')
