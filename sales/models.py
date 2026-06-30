# sales/models.py (ဥပမာ ပုံစံ)
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True) # ဘယ်နေ့ ဘယ်အချိန် ရောင်းရလဲ စစ်ရန်

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # ရောင်းရစဉ်က ဈေးနှုန်း
    
    from django.db import models
from django.contrib.auth.models import User

class Sale(models.Model):
    cashier = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) # ဘယ်နေ့ရောင်းခဲ့လဲ သိဖို့

    def __str__(self):
        return f"Sale {self.id} by {self.cashier}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)