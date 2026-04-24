# Odoo Bootstraps

Bootstrap modules for Odoo 18 projects. One-click installation of curated module baskets.

## Available Bootstraps

| Module | Modules | For |
|--------|---------|-----|
| `basket_universal_bootstrap` | 5 | Any country |
| `basket_ar_bootstrap` | 28 + 3 recommended Aries | Argentina (includes Universal) |

## Usage

### 1. Add as submodule to your project

```bash
git submodule add -b 18.0 https://github.com/Aries-Consulting/odoo-bootstraps.git aries/bootstraps
git submodule update --init --recursive
```

### 2. Install from Odoo Apps

1. Update Apps List
2. Search for "Basket Universal Bootstrap" or "Basket AR Bootstrap"
3. Install

### 3. After installation

The bootstrap module can be uninstalled - the installed modules will remain.
Each module can then be managed individually.

## Basket Contents

### Universal (5 modules)

**UX/Productivity:**
- `web_m2x_options` - Dropdown control
- `web_notify` - Notifications
- `web_responsive` - Mobile-friendly backend

**Reports:**
- `report_xlsx` - Excel export

**Optional (install manually if needed):**
- `auditlog` - Audit trail (compliance requirement)
- `database_cleanup` - DB cleanup (use with caution)

### AR (28 modules: 8 Universal + 20 AR)

**Auto-installed (28 modules):**

Payments:
- `account_payment_pro` - Grouped payments
- `account_payment_pro_receiptbook` - Receipt books

Core AR:
- `l10n_ar_ux` - Base AR UX
- `l10n_ar_tax` - Perceptions/retentions
- `l10n_ar_bank` - AR banks
- `l10n_ar_edi_ux` - E-invoicing UX
- `l10n_ar_currency_update` - AFIP exchange rates
- `l10n_ar_account_reports` - AR financial reports

UX (Ingadhoc):
- `account_ux`, `account_internal_transfer`, `account_accountant_ux`
- `sale_ux`, `purchase_ux`, `stock_ux`, `stock_no_negative`
- `product_ux`, `base_ux`

Reports:
- `account_journal_book_report` - Legal journal book (Libro Diario)

OCA:
- `currency_rate_live`, `stock_picking_invoice_link`

**Recommended Aries modules (install manually):**
- `aries_afip_padron_ux` - Robust AFIP padron batch update
- `l10n_ar_invoice_cancel` - Restrict electronic invoice cancellation
- `l10n_ar_ux_fix_report_invoice_vat` - Fix CUIT/VAT display in PDFs

## Required Submodules

For the bootstraps to work, your project needs these repos as submodules:

### Universal

```bash
git submodule add -b 18.0 https://github.com/OCA/server-tools.git oca/server-tools  # optional modules
git submodule add -b 18.0 https://github.com/OCA/web.git oca/web
git submodule add -b 18.0 https://github.com/OCA/reporting-engine.git oca/reporting-engine
```

### AR (additional)

```bash
git submodule add -b 18.0 https://github.com/ingadhoc/odoo-argentina.git adhoc/odoo-argentina
git submodule add -b 18.0 https://github.com/ingadhoc/odoo-argentina-ee.git adhoc/odoo-argentina-ee
git submodule add -b 18.0 https://github.com/ingadhoc/argentina-sale.git adhoc/argentina-sale
git submodule add -b 18.0 https://github.com/ingadhoc/account-payment.git adhoc/account-payment
git submodule add -b 18.0 https://github.com/ingadhoc/account-financial-tools.git adhoc/account-financial-tools
git submodule add -b 18.0 https://github.com/ingadhoc/sale.git adhoc/sale
git submodule add -b 18.0 https://github.com/ingadhoc/purchase.git adhoc/purchase
git submodule add -b 18.0 https://github.com/ingadhoc/stock.git adhoc/stock
git submodule add -b 18.0 https://github.com/ingadhoc/product.git adhoc/product
git submodule add -b 18.0 https://github.com/ingadhoc/miscellaneous.git adhoc/miscellaneous
git submodule add -b 18.0 https://github.com/OCA/currency.git oca/currency
git submodule add -b 18.0 https://github.com/OCA/stock-logistics-workflow.git oca/stock-logistics-workflow
git submodule add -b 18.0 https://github.com/ingadhoc/aeroo_reports.git adhoc/aeroo_reports
```

## License

LGPL-3

## Author

Aries Consulting
