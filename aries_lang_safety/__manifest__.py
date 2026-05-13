# -*- coding: utf-8 -*-
{
    'name': 'Aries Language Safety',
    'version': '18.0.3.0.0',
    'category': 'Technical',
    'summary': 'Prevents Invalid language code 400 errors at the raise site',
    'description': """
        Minimal language safety for Odoo 18 deployments.

        Problem this solves:
        Odoo 18 raises `UserError(f'Invalid language code: {lang}')` from
        `Environment.lang` (odoo/api.py:765) whenever `context.lang` is
        set to a code not active in `res_lang`. The HTTP dispatcher
        converts that UserError to a `BadRequest` 400 — observed when
        browsers send `Accept-Language: es-ES` and the database does
        not have `es_ES` active. The bad lang code can be injected into
        `context.lang` from multiple sources (session defaults, URL
        params, cookies, odoo.sh platform middleware), so positional
        defenses (session sanitizers, _pre_dispatch overrides) are not
        reliable.

        What this module does:
        Replaces `Environment.lang` with a version that falls back to
        the first active lang (preferring `es_AR`, then `en_US`) when
        the requested lang is not active, instead of raising. This is
        the single point at which every code path that produces the
        400 converges, so patching it definitively prevents the error
        regardless of where the bad lang came from.

        What this module deliberately does NOT do:
        - Does NOT activate any language
        - Does NOT migrate users or partners
        - Does NOT deactivate any language
        - Does NOT load translations
        - Does NOT override any model

        Configuration of installed languages, user lang preferences and
        translation reloading remains the user's responsibility via
        Settings > Translations.

        Migration from v1.x or v2.x:
        On upgrade, no scripts run. The previous module's effects on
        user / partner lang data are preserved as-is. The new patch
        replaces the previous override and monkey-patches.
    """,
    'author': 'Aries Consulting',
    'website': 'https://github.com/Aries-Consulting/odoo-bootstraps',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
