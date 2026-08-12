from .auth import cashier_login, pos_page, scan_product_api, save_transaction, get_scanned_code
from .dashboard import admin_dashboard
from .products import add_product, edit_product, delete_product, add_managed_product, edit_managed_product, delete_managed_product
from .categories import add_category, edit_category, delete_category, add_subcategory, edit_subcategory, delete_subcategory
from .suppliers import add_supplier, edit_supplier, delete_supplier
from .cashiers import add_cashier, edit_cashier, delete_cashier
from .purchases import add_purchase, edit_purchase, delete_purchase
from .variants import add_size, edit_size, delete_size, add_variant, edit_variant, delete_variant

__all__ = [
    'cashier_login', 'pos_page', 'scan_product_api', 'save_transaction', 'get_scanned_code',
    'admin_dashboard',
    'add_product', 'edit_product', 'delete_product',
    'add_managed_product', 'edit_managed_product', 'delete_managed_product',
    'add_category', 'edit_category', 'delete_category',
    'add_subcategory', 'edit_subcategory', 'delete_subcategory',
    'add_supplier', 'edit_supplier', 'delete_supplier',
    'add_cashier', 'edit_cashier', 'delete_cashier',
    'add_purchase', 'edit_purchase', 'delete_purchase',
    'add_size', 'edit_size', 'delete_size',
    'add_variant', 'edit_variant', 'delete_variant',
]
