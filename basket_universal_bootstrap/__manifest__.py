# -*- coding: utf-8 -*-
{
    'name': 'Basket Universal Bootstrap',
    'version': '18.0.2.0.0',
    'category': 'Technical',
    'summary': 'Installs all Universal basket modules (6 modules)',
    'description': """
        Bootstrap module for any Odoo 18 project (any country).

        Installing this single module will install all 6 Universal modules:

        **Security/Compliance:**
        - auditlog: Audit trail for create/write/unlink operations
        - password_security: Password policies (length, complexity, expiration)

        **UX/Productivity:**
        - web_m2x_options: Control dropdowns (disable create, limit results)
        - web_notify: Server-to-client notifications

        **Reports:**
        - report_xlsx: Export any report to Excel

        **Maintenance:**
        - database_cleanup: Remove orphaned DB artifacts

        **Usage:**
        Install this module once during project setup.
        After installation, you can uninstall this bootstrap module -
        the 6 modules will remain installed and can be managed individually.

        **Recommended (install on demand, not bundled):**
        - auth_session_timeout (OCA/server-auth): Auto-logout after inactivity
        - server_action_mass_edit (OCA/server-ux): Bulk edit multiple records

        **For Argentine projects:** Use basket_ar_bootstrap instead (includes these 6 + 20 AR modules).
    """,
    'author': 'Aries Consulting',
    'website': 'https://github.com/Aries-Consulting/odoo-bootstraps',
    'license': 'LGPL-3',
    'depends': [
        # ==========================================
        # UNIVERSAL BASKET (6 modules)
        # ==========================================
        # Security/Compliance
        'auditlog',                    # OCA/server-tools - Audit trail
        'password_security',           # OCA/server-auth - Password policies
        # UX/Productivity
        'web_m2x_options',             # OCA/web - Dropdown control
        'web_notify',                  # OCA/web - Server notifications
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
