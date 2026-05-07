# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

TARGET_LANG = 'es_AR'
FALLBACK_LANG = 'en_US'


def _apply_lang_safety(env):
    """Activate es_AR, migrate stale lang references, and clean up.

    Idempotent — safe to run on fresh installs and on upgrades over
    databases that may already be in any state (es_ES active, es_ES
    referenced by users, neither installed, etc.).
    """
    ResLang = env['res.lang'].with_context(active_test=False)

    # 1) Ensure target lang exists and is active
    target = ResLang.search([('code', '=', TARGET_LANG)], limit=1)
    if not target:
        # Should never happen on Odoo 18 (es_AR is in res.lang.csv) but
        # _activate_lang creates it from the master CSV if missing.
        env['res.lang']._activate_lang(TARGET_LANG)
        target = ResLang.search([('code', '=', TARGET_LANG)], limit=1)
    elif not target.active:
        # _activate_lang loads translations for installed modules
        env['res.lang']._activate_lang(TARGET_LANG)

    # 2) Migrate any user / partner whose lang is now invalid
    active_codes = [c for c, _ in env['res.lang'].get_installed()]
    env.cr.execute(
        """
        UPDATE res_users
           SET lang = %s
         WHERE lang IS NULL
            OR lang NOT IN %s
        """,
        (TARGET_LANG, tuple(active_codes) or ('',)),
    )
    users_fixed = env.cr.rowcount
    env.cr.execute(
        """
        UPDATE res_partner
           SET lang = %s
         WHERE lang IS NOT NULL
           AND lang NOT IN %s
        """,
        (TARGET_LANG, tuple(active_codes) or ('',)),
    )
    partners_fixed = env.cr.rowcount

    # 3) Set company partner lang to target so context_get resolves cleanly
    env.cr.execute(
        """
        UPDATE res_partner p
           SET lang = %s
          FROM res_company c
         WHERE c.partner_id = p.id
           AND (p.lang IS NULL OR p.lang != %s)
        """,
        (TARGET_LANG, TARGET_LANG),
    )

    # 4) Deactivate es_ES if active and no longer referenced anywhere
    es_es = ResLang.search([('code', '=', 'es_ES'), ('active', '=', True)], limit=1)
    if es_es:
        env.cr.execute(
            "SELECT 1 FROM res_users WHERE lang = 'es_ES' "
            "UNION ALL SELECT 1 FROM res_partner WHERE lang = 'es_ES' "
            "LIMIT 1"
        )
        if not env.cr.fetchone():
            try:
                es_es.active = False
            except Exception as e:
                # Don't block install if Odoo refuses to deactivate
                # (e.g. due to a translated record in a not-yet-migrated
                # state). The ir.http override still protects at runtime.
                _logger.warning("Could not deactivate es_ES: %s", e)

    # 5) Invalidate ormcache so context_get rebuilds with new user lang
    env.registry.clear_cache()

    _logger.info(
        "aries_lang_safety: %s active, fixed %d users and %d partners",
        TARGET_LANG, users_fixed, partners_fixed,
    )


def post_init_hook(env):
    _apply_lang_safety(env)
