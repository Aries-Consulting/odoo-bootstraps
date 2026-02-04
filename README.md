# Odoo Bootstraps

Bootstrap modules for Odoo 18 projects. One-click installation of curated module baskets.

## Available Bootstraps

| Module | Modules | For |
|--------|---------|-----|
| `basket_universal_bootstrap` | 9 | Any country |
| `basket_ar_bootstrap` | 28 | Argentina (includes Universal) |

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

### Universal (9 modules)

**Security/Compliance:**
- `auditlog` - Audit trail
- `password_security` - Password policies
- `auth_session_timeout` - Session timeout

**UX/Productivity:**
- `web_m2x_options` - Dropdown control
- `web_environment_ribbon` - Environment indicator
- `web_notify` - Notifications
- `server_action_mass_edit` - Bulk edit

**Reports:**
- `report_xlsx` - Excel export

**Maintenance:**
- `database_cleanup` - DB cleanup

### AR (19 additional modules)

**Payments:**
- `account_payment_pro` - Grouped payments
- `account_payment_pro_receiptbook` - Receipt books

**Core AR:**
- `l10n_ar_ux` - Base AR UX
- `l10n_ar_tax` - Perceptions/retentions
- `l10n_ar_bank` - AR banks
- `l10n_ar_edi_ux` - E-invoicing UX
- `l10n_ar_currency_update` - AFIP exchange rates
- `l10n_ar_account_reports` - AR financial reports

**UX (Ingadhoc):**
- `account_ux`, `account_internal_transfer`, `account_accountant_ux`
- `sale_ux`, `purchase_ux`, `stock_ux`, `stock_no_negative`
- `product_ux`, `base_ux`

**OCA:**
- `currency_rate_live`, `stock_picking_invoice_link`

## Required Submodules

For the bootstraps to work, your project needs these repos as submodules:

### Universal

```bash
git submodule add -b 18.0 https://github.com/OCA/server-tools.git oca/server-tools
git submodule add -b 18.0 https://github.com/OCA/server-auth.git oca/server-auth
git submodule add -b 18.0 https://github.com/OCA/web.git oca/web
git submodule add -b 18.0 https://github.com/OCA/server-ux.git oca/server-ux
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
```

## License

LGPL-3

## Author

Aries Consulting
