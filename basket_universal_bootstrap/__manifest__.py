# -*- coding: utf-8 -*-
{
    'name': 'Basket Universal Bootstrap',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Installs all Universal basket modules (9 modules)',
    'description': """
        Bootstrap module for any Odoo 18 project (any country).

        Installing this single module will install all 9 Universal modules:

        **Security/Compliance:**
        - auditlog: Audit trail for create/write/unlink operations
        - password_security: Password policies (length, complexity, expiration)
        - auth_session_timeout: Auto-logout after inactivity

        **UX/Productivity:**
        - web_m2x_options: Control dropdowns (disable create, limit results)
        - web_environment_ribbon: Visual DEV/STAGING/PROD indicator
        - web_notify: Server-to-client notifications
        - server_action_mass_edit: Bulk edit multiple records

        **Reports:**
        - report_xlsx: Export any report to Excel

        **Maintenance:**
        - database_cleanup: Remove orphaned DB artifacts

        **Usage:**
        Install this module once during project setup.
        After installation, you can uninstall this bootstrap module -
        the 9 modules will remain installed and can be managed individually.

        **For Argentine projects:** Use basket_ar_bootstrap instead (includes these 9 + 19 AR modules).
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
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
