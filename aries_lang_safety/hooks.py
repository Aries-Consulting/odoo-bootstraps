# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

TARGET_LANG = 'es_AR'


def _apply_lang_safety(env):
    """Activate es_AR, consolidate all Spanish variants to es_AR, and
    deactivate every other Spanish variant. Idempotent.

    This handles three cases:
    1. Fresh install where the DB only has en_US.
    2. Production copy where users/partners have lang='es_ES'.
    3. Recovery scenario where someone manually activated 'es_ES' in
       the shell to get back into the UI — we still want to consolidate
       and deactivate it.

    Note: res.users.lang is a non-stored related field that proxies
    res.partner.lang. All updates go through the ORM so the relation
    resolves correctly.
    """
    ResLang = env['res.lang'].with_context(active_test=False)

    # 1) Ensure target lang is active
    target = ResLang.search([('code', '=', TARGET_LANG)], limit=1)
    if not target or not target.active:
        env['res.lang']._activate_lang(TARGET_LANG)

    Users = env['res.users'].with_context(active_test=False)
    Partners = env['res.partner'].with_context(active_test=False)

    # 2) Consolidate ALL Spanish variants (es, es_ES, es_419, es_MX, ...)
    # to es_AR — regardless of whether the source variant is currently
    # active. Done explicitly with =like 'es%' so the active state of
    # es_ES at install time doesn't change behaviour.
    spanish_domain = [
        ('lang', '=like', 'es%'),
        ('lang', '!=', TARGET_LANG),
    ]
    sp_users = Users.search(spanish_domain)
    if sp_users:
        sp_users.write({'lang': TARGET_LANG})

    sp_partners = Partners.search(spanish_domain)
    if sp_partners:
        sp_partners.write({'lang': TARGET_LANG})

    # 3) Catch any leftover user/partner whose lang is NULL or pointing
    # to an inactive non-Spanish code (e.g. de_DE that was once active).
    # Done after the Spanish consolidation so active_codes is up to date.
    active_codes = [c for c, _name in env['res.lang'].get_installed()]

    leftover_users = Users.search([
        '|', ('lang', '=', False), ('lang', 'not in', active_codes),
    ])
    if leftover_users:
        leftover_users.write({'lang': TARGET_LANG})

    leftover_partners = Partners.search([
        ('lang', '!=', False), ('lang', 'not in', active_codes),
    ])
    if leftover_partners:
        leftover_partners.write({'lang': TARGET_LANG})

    # 4) Set every company partner to es_AR so context_get of users
    # without explicit lang resolves cleanly via the company fallback.
    company_partners = env['res.company'].search([]).partner_id
    company_partners.filtered(
        lambda p: p.lang != TARGET_LANG
    ).write({'lang': TARGET_LANG})

    # 5) Deactivate every active Spanish variant other than es_AR.
    # By now no user/partner should reference them (we migrated above),
    # but we still gate on search_count just in case some cache is stale.
    other_spanish = ResLang.search([
        ('code', '=like', 'es%'),
        ('code', '!=', TARGET_LANG),
        ('active', '=', True),
    ])
    for lang_rec in other_spanish:
        still_used = (
            Users.search_count([('lang', '=', lang_rec.code)], limit=1)
            or Partners.search_count([('lang', '=', lang_rec.code)], limit=1)
        )
        if still_used:
            _logger.warning(
                "aries_lang_safety: %s still referenced after migration, "
                "leaving it active.", lang_rec.code,
            )
            continue
        try:
            lang_rec.active = False
        except Exception as e:
            _logger.warning(
                "Could not deactivate %s: %s", lang_rec.code, e,
            )

    # 6) Invalidate ormcache so res.users.context_get rebuilds
    env.registry.clear_cache()

    _logger.info(
        "aries_lang_safety: %s active. Migrated %d users (%d Spanish, "
        "%d leftover) and %d partners (%d Spanish, %d leftover).",
        TARGET_LANG,
        len(sp_users) + len(leftover_users), len(sp_users), len(leftover_users),
        len(sp_partners) + len(leftover_partners), len(sp_partners), len(leftover_partners),
    )


def post_init_hook(env):
    _apply_lang_safety(env)
