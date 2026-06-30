

from django.contrib import admin
from .models import Sale, SaleItem # ညီမရဲ့ models တွေကို import လုပ်ပါ

admin.site.register(Sale)
admin.site.register(SaleItem)
