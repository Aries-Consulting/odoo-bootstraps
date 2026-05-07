# -*- coding: utf-8 -*-
{
    'name': 'Aries Language Safety (es_AR)',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Activates es_AR and protects against browser locale mismatches',
    'description': """
        Language safety for Argentine Odoo deployments.

        Problem this solves:
        Odoo 18 sets `session.context['lang']` from the browser's
        Accept-Language header (via babel) without validating that the
        language is actually installed in the database. Argentine clients
        whose browsers send `es-ES` (or just `es`, which babel aliases to
        `es_ES`) hit `Invalid language code: es_ES` HTTP 400 errors when
        accessing /odoo, because neither `l10n_ar` nor any AR module
        activates `es_AR` automatically.

        What this module does:
        1. Activates `es_AR` (and only `es_AR`) as the working Spanish.
        2. Updates admin user, root user and the company partner to use
           `es_AR` so cached `res.users.context_get` resolves to a valid
           lang.
        3. Migrates any existing user / partner whose `lang` points to an
           inactive language code (typically `es_ES` from a sanitized
           production copy) to `es_AR`.
        4. Deactivates `es_ES` if active and unused, so the database stays
           single-language.
        5. Overrides `ir.http._pre_dispatch` to silently rewrite any
           browser-provided session lang that is not active in the
           database to `es_AR` (or `en_US` as ultimate fallback). This
           protects against any future locale mismatch (es-ES, es-419,
           de-DE, etc.) without forcing those languages to be installed.
    """,
    'author': 'Aries Consulting',
    'website': 'https://github.com/Aries-Consulting/odoo-bootstraps',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
