# -*- coding: utf-8 -*-
{
    'name': 'Aries Language Safety',
    'version': '18.0.2.0.1',
    'category': 'Technical',
    'summary': 'Prevents Invalid language code 400 errors from browser locale mismatches',
    'description': """
        Minimal language safety for Odoo 18 deployments.

        Problem this solves:
        Odoo 18 sets `session.context['lang']` from the browser's
        Accept-Language header (via babel) without validating that the
        language is installed in the database. Browsers sending `es-ES`
        (or just `es`, which babel aliases to `es_ES`) crash `/odoo`
        with `Invalid language code: es_ES` HTTP 400 when neither
        `es_ES` nor a fallback es_* variant is active.

        What this module does:
        Two layers of defense, both running on every request:

        1. Monkey-patches `Request._get_session_and_dbname` (loaded at
           module import) to sanitize `session.context['lang']` BEFORE
           any ir.http override or env access. This is the primary line
           of defense: it runs at the earliest possible point in the
           request lifecycle, independent of MRO order.

        2. Overrides `ir.http._pre_dispatch` as a secondary defense in
           case the monkey-patch is bypassed by an unusual code path.

        Both layers rewrite an invalid lang to `es_AR`, then `en_US`,
        then any active language as ultimate fallback.

        What this module deliberately does NOT do:
        - Does NOT activate any language. Use Settings > Translations
          to add languages — this triggers Odoo's standard `toggle_active`
          which loads .po translations correctly.
        - Does NOT migrate users or partners. Existing data is untouched.
        - Does NOT deactivate any language. The override handles invalid
          requests at runtime; you do not need to deactivate `es_ES`.
        - Does NOT load translations. Use Settings > Translations >
          Reload Translations or activate the lang via UI.

        Migration from v1.x:
        Earlier versions had a heavy post-install hook that activated
        es_AR, migrated users and deactivated es_ES. That hook caused
        translation loading inconsistencies and was removed in v2.0.0.
        If you upgraded from v1.x and are seeing partially translated
        UI, run from `odoo-bin shell`:

            mods = env['ir.module.module'].search([('state', '=', 'installed')])
            mods._update_translations(['es_AR'])
            env.cr.commit()
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
