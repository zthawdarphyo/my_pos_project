from django.shortcuts import render, redirect, get_object_or_404

from ..models import Category, Subcategory
from .dashboard import admin_dashboard


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
    return admin_dashboard(request, section='categories')


def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return admin_dashboard(request, section='categories')


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
    return admin_dashboard(request, section='categories')


def add_subcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, id=category_id)
            Subcategory.objects.create(name=name, category=category)
    return admin_dashboard(request, section='subcategories')


def delete_subcategory(request, subcategory_id):
    if request.method == 'POST':
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        subcategory.delete()
    return admin_dashboard(request, section='subcategories')


def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = get_object_or_404(Category, id=category_id)
            subcategory.name = name
            subcategory.category = category
            subcategory.save()
    return admin_dashboard(request, section='subcategories')
