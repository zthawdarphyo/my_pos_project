# sales/models.py (ဥပမာ ပုံစံ)
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    pdf_file = models.FileField(upload_to='invoices_pdf/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number or f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # ရောင်းရစဉ်က ဈေးနှုန်း

    @property
    def total_price(self):
        return self.price * self.quantity
    
    from django.db import models
from django.contrib.auth.models import User

class Sale(models.Model):
    cashier = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    image_file = models.FileField(upload_to='invoices_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # ဘယ်နေ့ရောင်းခဲ့လဲ သိဖို့

    @property
    def subtotal(self):
        return self.total_amount - self.tax

    def __str__(self):
        return f"Sale {self.id} by {self.cashier}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)