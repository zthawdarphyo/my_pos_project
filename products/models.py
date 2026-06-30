import os
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
import qrcode

# ၁။ Category Management
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __cl__ (self):
        return self.name

# ၄။ Supplier Management
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# ၂။ Product & ၃။ QR Code Management
class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True) # P000001
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2) # ၆။ Price Management
    stock = models.IntegerField(default=0) # ၄။ Inventory Management
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    # Product သိမ်းလိုက်တာနဲ့ QR Code Auto ထွက်အောင် လုပ်ခြင်း
    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.product_code)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            filename = f"qr_{self.product_code}.png"
            self.qr_code.save(filename, File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_code} - {self.name}"