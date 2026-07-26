# NEXT-GEN POS System

A Django-based Point of Sale (POS) web application with Burmese language support, role-based access, product management, sales analytics, and invoice generation.

## 🛠️ Tech Stack

- **Backend**: Django 6.0.7
- **Database**: MySQL (`my_pos_db`)
- **Frontend**: HTML, CSS (Font Awesome 6.4.0)
- **Charts**: Matplotlib + Seaborn (Myanmar font support)
- **QR Codes**: qrcode + Pillow
- **Invoices**: ReportLab (PDF), Pillow (PNG)

## 📦 Installation

```bash
# 1. Clone repository


# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install django mysqlclient qrcode pillow reportlab matplotlib seaborn

# 4. Configure database in core/settings.py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'my_pos_db',
#         'USER': 'root',
#         'PASSWORD': 'Admin123',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## 👥 User Roles & Login

| Role | Access | Default URL |
|------|--------|-------------|
| **Superuser / Admin** | Full admin dashboard, all CRUD operations | `/products/dashboard/` |
| **Cashier** | POS terminal, sales | `/sales/pos/` |
| **Staff** | Admin dashboard (read/write) | `/products/dashboard/` |

### Login URLs
- **Main Login**: `/`
- **Cashier Login**: `/products/cashier-login/`
- **Logout**: `/logout/`

## 🎯 Features

### 1. Admin Dashboard (`/products/dashboard/`)

The main control center with multiple tabs:

#### Dashboard Tab
- **Total Sales** - All-time revenue from sales
- **Total Transactions** - Count of all sales orders
- **Low Stock Alert** - Products with stock below 10
- **Product Bundle Analytics** - Chart showing frequently bought together products with confidence percentages
  - `See More` / `See Less` toggle to expand/collapse bundle list
- **Best Selling Products** - Top products by quantity sold
- **Top Sales Days** - Weekly transaction distribution
- **Category-Subcategory Relationship Confidence** - Progress bars showing how complete product categorizations are

#### Products Tab
- **Product List** - Paginated table of all products
- **Add/Edit/Delete Products** - Full CRUD with:
  - Product Code (auto-generated QR)
  - Name, Price, Stock
  - Category, Subcategory, Supplier
  - Auto QR code generation on save

#### Managed Products Tab
- Independent product management separate from inventory
- Category and subcategory assignment
- Used for product bundle analytics

#### Categories Tab
- Add/Edit/Delete categories
- Unique category names

#### Subcategories Tab
- Add/Edit/Delete subcategories
- Linked to parent categories
- Unique together constraint (name + category)

#### Cashiers Tab
- Add/Edit/Delete cashier accounts
- Phone number storage via CashierProfile
- Role-based access control

#### Suppliers Tab
- Add/Edit/Delete suppliers
- Name, Phone, Email fields

#### Sizes Tab
- Add/Edit/Delete product sizes (S, M, L, XL, etc.)

#### Variants Tab
- Product variant management
- Size, Buying Price, Selling Price
- Barcode management
- QR code generation per variant
- Expiry date tracking

#### Purchase Tab
- Purchase order management
- Supplier, product, quantity, price tracking
- Cashier assignment
- Date-stamped entries

#### Balance Tab
- Ledger-style balance tracking
- Columns: ID, Product Name, Subcategory, Cashier, Type, Purchase, Sale, Date, Balance
- Running balance calculation per product
- Purchase entries show `+qty`
- Sale entries show `-qty`
- Newest entries first
- Subcategory pulled from ManagedProduct or Product

#### Reports Tab
- **Advanced Filtering**:
  - Date range search
  - Today's Sales filter
  - Month filter
  - Year filter
  - Cashier filter
  - Product Code search
  - Barcode search
- **Sales Analytics**:
  - Total filtered sales amount
  - Total filtered invoices count
  - Product inventory stats
  - Category/subcategory relationship confidence
  - Best selling products chart
  - Weekly transaction chart
  - Low stock alert table
- **Sales History Table**: Voucher ID, Product Name, Price, Qty, Subtotal, Cashier, Date

### 2. POS Terminal (`/sales/pos/`)

Cashier-facing point of sale interface:
- **Manual barcode entry** - Type product code and add to cart
- **QR Scanner support** - Camera-based barcode scanning via HTML5-QRCode
- **Shopping cart** - Session-based cart management
- **Auto calculations** - Subtotal, 5% tax, Grand total
- **Checkout** - Creates Order, reduces stock, generates PDF invoice + PNG image
- **Clear cart** - Reset current sale

### 3. Invoice Management (`/sales/invoices/`)

- **Invoice List** - All orders and sales with dates
- **Invoice Detail** - View individual invoice with items
- **PDF Download** - Auto-generated PDF per order
- **PNG Image** - Auto-generated invoice image per order

### 4. QR Code Features

- **Product QR Codes** - Auto-generated on product creation
  - Stored in `media/qr_codes/`
  - Linked to product_code
- **Variant QR Codes** - Generated per variant
  - Stored in `media/variant_qr_codes/`
  - Linked to variant barcode
- **QR Scanner API** - `/products/api/scan-product/<code>/`
  - Returns product details for POS integration

### 5. Authentication & Security

- Django's built-in authentication system
- Role-based redirects (admin vs cashier)
- Login required decorators on protected views
- CSRF protection on forms
- Session-based cart for POS

## 📊 Database Models

### Products App
| Model | Purpose |
|-------|---------|
| `Category` | Product categories (unique names) |
| `Subcategory` | Subcategories linked to categories |
| `Supplier` | Supplier contact info |
| `ProductSize` | Size options (S, M, L, etc.) |
| `Product` | Main product with QR code, stock, price |
| `ProductVariant` | Variants with barcode, size, expiry |
| `CashierProfile` | Extended user phone number |
| `ManagedProduct` | Independent product for analytics |
| `Purchase` | Purchase orders with supplier/cashier |

### Sales App
| Model | Purpose |
|-------|---------|
| `Order` | Legacy order model with PDF invoice |
| `OrderItem` | Legacy order line items |
| `Sale` | New sale model with image invoice |
| `SaleItem` | Sale line items with product_name snapshot |

## 🔧 Configuration

### Settings (`core/settings.py`)
- `DEBUG = True` (development)
- `ALLOWED_HOSTS = []`
- Database: MySQL backend
- Installed apps: `authentication`, `products`, `sales`
- Media root: `/media/`
- QR code directories: `qr_codes/`, `variant_qr_codes/`

### URL Structure
```
/                                    → Login page
/products/dashboard/                 → Admin dashboard
/products/cashier-login/             → Cashier login
/products/pos-terminal/              → POS terminal (cashier)
/sales/pos/                          → POS dashboard
/sales/checkout/                     → Checkout & invoice
/sales/invoices/                     → Invoice list
/products/api/scan-product/<code>/   → QR scan API
/logout/                             → Logout
```

## 🚀 Usage Guide

### For Admins

1. **Login** at `/` with superuser/staff credentials
2. **Dashboard** - View analytics, sales trends, low stock alerts
3. **Products** - Add/edit products with auto QR codes
4. **Categories/Subcategories** - Organize products hierarchically
5. **Suppliers** - Manage supplier information
6. **Cashiers** - Create cashier accounts for POS
7. **Variants** - Manage product variants with barcodes
8. **Purchases** - Record stock purchases from suppliers
9. **Balance** - Track stock movements and running balance
10. **Reports** - Filter sales by date, cashier, product, barcode

### For Cashiers

1. **Login** at `/products/cashier-login/`
2. **POS Terminal** - Enter product codes manually or scan QR
3. **Cart Management** - View cart, adjust quantities
4. **Checkout** - Complete sale, stock auto-updates
5. **Invoice** - Auto-generated PDF receipt

### QR Code Workflow

1. Admin creates Product → QR code auto-generated
2. Print QR code and place on product
3. Cashier scans QR at POS → Product auto-adds to cart
4. Checkout → Sale recorded, stock reduced

## 📝 Notes

- Tax rate is fixed at **5%**
- Currency: **MMK (Myanmar Kyat)**
- Low stock threshold: **< 10 units**
- Pagination: **4 items per page** (admin tables)
- Balance pagination: **10 items per page**
- Charts use **Noto Sans Myanmar** font for Burmese text
- Dashboard chart shows top **5 bundles** by default (See More for all)

## 🔑 Default Credentials

Create superuser via:
```bash
python manage.py createsuperuser
```

Suggested test accounts:
- **Admin**: `zin` / `admin123`
- **Cashier**: `cashier1` / `cash123`

## 📁 Project Structure

```
my_pos_project/
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── authentication/
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── login.html
├── products/
│   ├── views.py          # Main admin dashboard & all CRUD
│   ├── models.py
│   ├── urls.py
│   └── templates/
│       ├── admin_dashboard.html
│       ├── cashier_pos.html
│       └── pos_invoice.html
├── sales/
│   ├── views.py          # POS, checkout, invoices
│   ├── models.py
│   ├── urls.py
│   └── templates/
│       ├── pos_dashboard.html
│       ├── invoice_list.html
│       └── invoice.html
├── media/
│   ├── qr_codes/
│   ├── variant_qr_codes/
│   └── invoices_pdf/
├── manage.py
└── venv/
```

## 🐛 Troubleshooting

- **MySQL not connecting**: Ensure MySQL service is running and credentials in `settings.py` are correct
- **Font boxes in charts**: Clear matplotlib cache with `rm -rf ~/.cache/matplotlib`
- **Migration errors**: Drop tables and re-run `python manage.py migrate`
- **QR code not found**: Ensure `media/qr_codes/` directory exists and is writable
