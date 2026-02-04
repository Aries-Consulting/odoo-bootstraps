# -*- coding: utf-8 -*-
{
    'name': 'Basket AR Bootstrap',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Installs all Basket AR modules (Universal + Argentina = 28 modules)',
    'description': """
        Bootstrap module for Argentine Odoo 18 projects.

        Installing this single module will install all 28 modules:

        **UNIVERSAL BASKET (9 modules):**

        Security/Compliance:
        - auditlog: Audit trail for create/write/unlink operations
        - password_security: Password policies (length, complexity, expiration)
        - auth_session_timeout: Auto-logout after inactivity

        UX/Productivity:
        - web_m2x_options: Control dropdowns (disable create, limit results)
        - web_environment_ribbon: Visual DEV/STAGING/PROD indicator
        - web_notify: Server-to-client notifications
        - server_action_mass_edit: Bulk edit multiple records

        Reports:
        - report_xlsx: Export any report to Excel

        Maintenance:
        - database_cleanup: Remove orphaned DB artifacts

        **AR BASKET (19 modules):**

        Payments:
        - account_payment_pro: Grouped payments with multiple methods
        - account_payment_pro_receiptbook: Numbered receipt books

        Core AR:
        - l10n_ar_ux: Base Argentina UX, AFIP activities
        - l10n_ar_tax: Automatic perception/retention calculations
        - l10n_ar_bank: Argentine bank list, CBU validation
        - l10n_ar_edi_ux: E-invoicing improvements
        - l10n_ar_currency_update: Automatic AFIP exchange rates
        - l10n_ar_account_reports: AR format financial reports

        UX (Ingadhoc):
        - account_ux: Accounting UX improvements
        - account_internal_transfer: Internal bank transfers
        - account_accountant_ux: Accountant shortcuts
        - sale_ux: Sales UX improvements
        - purchase_ux: Purchase UX improvements
        - stock_ux: Stock UX improvements
        - stock_no_negative: Prevent negative inventory
        - product_ux: Product UX improvements
        - base_ux: Base UX improvements

        OCA Dependencies:
        - currency_rate_live: Exchange rate framework
        - stock_picking_invoice_link: Link pickings to invoices

        **Usage:**
        Install this module once during project setup.
        After installation, you can uninstall this bootstrap module -
        the 28 modules will remain installed and can be managed individually.
    """,
    'author': 'Aries Consulting',
    'website': 'https://github.com/Aries-Consulting/odoo-bootstraps',
    'license': 'LGPL-3',
    'depends': [
        # ==========================================
        # UNIVERSAL BASKET (9 modules)
        # ==========================================
        # Security/Compliance
        'auditlog',                    # OCA/server-tools - Audit trail
        'password_security',           # OCA/server-auth - Password policies
        'auth_session_timeout',        # OCA/server-auth - Session timeout
        # UX/Productivity
        'web_m2x_options',             # OCA/web - Dropdown control
        'web_environment_ribbon',      # OCA/web - DEV/STAGING/PROD ribbon
        'web_notify',                  # OCA/web - Server notifications
        'server_action_mass_edit',                # OCA/server-ux - Bulk edit
        # Reports
        'report_xlsx',                 # OCA/reporting-engine - Excel export
        # Maintenance
        'database_cleanup',            # OCA/server-tools - DB cleanup

        # ==========================================
        # AR BASKET (19 modules)
        # ==========================================
        # Payments
        'account_payment_pro',              # ingadhoc/account-payment
        'account_payment_pro_receiptbook',  # ingadhoc/account-payment
        # Core AR
        'l10n_ar_ux',                  # ingadhoc/odoo-argentina
        'l10n_ar_tax',                 # ingadhoc/odoo-argentina
        'l10n_ar_bank',                # ingadhoc/odoo-argentina
        'l10n_ar_edi_ux',              # ingadhoc/odoo-argentina-ee
        'l10n_ar_currency_update',     # ingadhoc/odoo-argentina-ee
        'l10n_ar_account_reports',     # ingadhoc/odoo-argentina-ee
        # UX Core (Ingadhoc)
        'account_ux',                  # ingadhoc/account-financial-tools
        'account_internal_transfer',   # ingadhoc/account-financial-tools
        'account_accountant_ux',       # ingadhoc/odoo-argentina-ee
        'sale_ux',                     # ingadhoc/sale
        'purchase_ux',                 # ingadhoc/purchase
        'stock_ux',                    # ingadhoc/stock
        'stock_no_negative',           # ingadhoc/stock
        'product_ux',                  # ingadhoc/product
        'base_ux',                     # ingadhoc/miscellaneous
        # OCA Dependencies
        'currency_rate_live',          # OCA/currency
        'stock_picking_invoice_link',  # OCA/stock-logistics-workflow
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
