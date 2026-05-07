# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

TARGET_LANG = 'es_AR'


def _apply_lang_safety(env):
    """Activate es_AR, migrate stale lang references, and clean up.

    Idempotent — safe on fresh installs and on upgrades over databases
    that may already be in any state (es_ES active, es_ES referenced by
    users, neither installed, etc.).

    Note: res.users.lang is a non-stored related field that proxies
    res.partner.lang (the actual storage). All updates therefore go
    through the ORM so the relation resolves correctly.
    """
    ResLang = env['res.lang'].with_context(active_test=False)

    # 1) Ensure target lang is active. _activate_lang both creates the
    # res.lang record (if missing) from the master CSV and loads
    # translations for installed modules.
    target = ResLang.search([('code', '=', TARGET_LANG)], limit=1)
    if not target or not target.active:
        env['res.lang']._activate_lang(TARGET_LANG)

    active_codes = [c for c, _name in env['res.lang'].get_installed()]

    # 2) Migrate users whose lang is missing or inactive
    Users = env['res.users'].with_context(active_test=False)
    users_to_fix = Users.search([
        '|', ('lang', '=', False), ('lang', 'not in', active_codes),
    ])
    if users_to_fix:
        users_to_fix.write({'lang': TARGET_LANG})

    # 3) Migrate partners whose lang is set but inactive (skip lang=False
    # — partners legitimately may have no lang set, unlike users)
    Partners = env['res.partner'].with_context(active_test=False)
    partners_to_fix = Partners.search([
        ('lang', '!=', False), ('lang', 'not in', active_codes),
    ])
    if partners_to_fix:
        partners_to_fix.write({'lang': TARGET_LANG})

    # 4) Set every company partner to target lang so context_get of
    # users without explicit lang resolves cleanly
    company_partners = env['res.company'].search([]).partner_id
    company_partners.filtered(
        lambda p: p.lang != TARGET_LANG
    ).write({'lang': TARGET_LANG})

    # 5) Deactivate es_ES if active and no longer referenced
    es_es = ResLang.search(
        [('code', '=', 'es_ES'), ('active', '=', True)], limit=1,
    )
    if es_es:
        still_used = (
            Users.search_count([('lang', '=', 'es_ES')], limit=1)
            or Partners.search_count([('lang', '=', 'es_ES')], limit=1)
        )
        if not still_used:
            try:
                es_es.active = False
            except Exception as e:
                # Don't block install if Odoo refuses to deactivate the
                # language for any reason. The ir.http override still
                # protects at runtime.
                _logger.warning("Could not deactivate es_ES: %s", e)

    # 6) Invalidate ormcache so res.users.context_get rebuilds with the
    # new partner langs
    env.registry.clear_cache()

    _logger.info(
        "aries_lang_safety: %s active, fixed %d users and %d partners",
        TARGET_LANG, len(users_to_fix), len(partners_to_fix),
    )


def post_init_hook(env):
    _apply_lang_safety(env)
