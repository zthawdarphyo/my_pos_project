# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from authentication.views import custom_login
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('', custom_login, name='home'),
#     path('auth/', include('authentication.urls')),
#     path('products/', include('products.urls',namespace='products')),
#     path('sales/', include('sales.urls')),
#     path('django-admin/', admin.site.urls), # built-in admin ကို အပိုအနေဖြင့် ထားထားခြင်း
#     # core/urls.py ထဲက လိုင်းဟောင်းကို အခုလို ပြောင်းပေးပါဗျာ-
#     # core/urls.py ကို ဖွင့်ပြီး logout လိုင်းကို ဤကဲ့သို့ အပြီးသတ် ပြောင်းပေးလိုက်ပါ-

#     path('logout/', auth_views.LogoutView.as_view(next_page='/products/cashier-login/'), name='logout'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import custom_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🌟 ဆာဗာ စ run တာနဲ့ NEXT-GEN POS Login ပေါ်မည့်နေရာ (URL Name ကို 'home' သို့မဟုတ် 'login' ဟု သုံးနိုင်သည်)
    path('', custom_login, name='home'),
    
    path('auth/', include('authentication.urls')),
    path('products/', include('products.urls', namespace='products')),
    path('sales/', include('sales.urls')),
    path('django-admin/', admin.site.urls), 
    
    # 🌟 ပြဿနာဖြစ်နေသည့် လိုင်းကို ဤကဲ့သို့ ပြင်လိုက်ပါ (next_page ကို root path '/' သို့ ညွှန်ပေးခြင်း)
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

