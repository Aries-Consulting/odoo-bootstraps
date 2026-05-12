# -*- coding: utf-8 -*-
import logging
import traceback

_logger = logging.getLogger(__name__)

TARGET_LANG = 'es_AR'


def _step(name):
    """Decorator: wrap a step so a failure in one step doesn't abort the
    whole cleanup. Surface the real traceback in the build log.
    """
    def deco(fn):
        def wrapper(env, *args, **kwargs):
            try:
                return fn(env, *args, **kwargs)
            except Exception:
                _logger.error(
                    "aries_lang_safety step %r failed:\n%s",
                    name, traceback.format_exc(),
                )
                return None
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco


@_step('activate_es_AR')
def _activate_target(env):
    """Activate es_AR via direct SQL to avoid the heavy _load_module_terms
    pass that _activate_lang() triggers, which can fail during a build if
    any installed module has a malformed .po file.

    es_AR is always present in res_lang from base/data/res.lang.csv, so
    we only need to flip its active flag.
    """
    env.cr.execute(
        "UPDATE res_lang SET active = TRUE "
        "WHERE code = %s AND active = FALSE",
        (TARGET_LANG,),
    )
    if env.cr.rowcount:
        _logger.info("aries_lang_safety: activated %s", TARGET_LANG)


@_step('migrate_spanish_variants')
def _migrate_spanish(env):
    """Force every Spanish variant (es, es_ES, es_419, es_MX, ...) to es_AR
    on users and partners, regardless of whether the source is active.
    """
    Users = env['res.users'].with_context(active_test=False)
    Partners = env['res.partner'].with_context(active_test=False)

    domain = [('lang', '=like', 'es%'), ('lang', '!=', TARGET_LANG)]
    sp_users = Users.search(domain)
    if sp_users:
        sp_users.write({'lang': TARGET_LANG})
        _logger.info(
            "aries_lang_safety: %d users migrated from non-AR Spanish",
            len(sp_users),
        )
    sp_partners = Partners.search(domain)
    if sp_partners:
        sp_partners.write({'lang': TARGET_LANG})
        _logger.info(
            "aries_lang_safety: %d partners migrated from non-AR Spanish",
            len(sp_partners),
        )


@_step('migrate_leftover_invalid_lang')
def _migrate_leftover(env):
    """Catch any user/partner whose lang is NULL or points to an inactive
    non-Spanish code (e.g. de_DE once active, now disabled).

    Uses direct SQL to read active codes (bypasses ormcache that may be
    stale during a registry build) and skips entirely if no langs are
    active (which would produce invalid SQL `NOT IN ()`).
    """
    env.cr.execute("SELECT code FROM res_lang WHERE active = TRUE")
    active_codes = [row[0] for row in env.cr.fetchall()]
    if not active_codes:
        _logger.warning(
            "aries_lang_safety: no active langs found, skipping leftover "
            "cleanup to avoid SQL NOT IN ()",
        )
        return

    Users = env['res.users'].with_context(active_test=False)
    Partners = env['res.partner'].with_context(active_test=False)

    leftover_u = Users.search([
        '|', ('lang', '=', False), ('lang', 'not in', active_codes),
    ])
    if leftover_u:
        leftover_u.write({'lang': TARGET_LANG})
        _logger.info(
            "aries_lang_safety: %d users with NULL/inactive lang fixed",
            len(leftover_u),
        )

    leftover_p = Partners.search([
        ('lang', '!=', False), ('lang', 'not in', active_codes),
    ])
    if leftover_p:
        leftover_p.write({'lang': TARGET_LANG})
        _logger.info(
            "aries_lang_safety: %d partners with inactive lang fixed",
            len(leftover_p),
        )


@_step('set_company_partner_lang')
def _set_company_partners(env):
    """Set every company partner to es_AR so context_get fallback resolves
    cleanly for users without an explicit lang.
    """
    company_partners = env['res.company'].search([]).partner_id
    to_fix = company_partners.filtered(lambda p: p.lang != TARGET_LANG)
    if to_fix:
        to_fix.write({'lang': TARGET_LANG})
        _logger.info(
            "aries_lang_safety: %d company partners set to %s",
            len(to_fix), TARGET_LANG,
        )


@_step('deactivate_non_ar_spanish')
def _deactivate_non_ar_spanish(env):
    """Deactivate every active Spanish variant other than es_AR — but
    only if it's no longer referenced (the migration steps above should
    have cleared every reference).

    Uses direct SQL for the deactivation check to avoid potential ORM
    constraint checks during write that would raise UserError if a
    reference is still around.
    """
    env.cr.execute(
        "SELECT id, code FROM res_lang "
        "WHERE active = TRUE AND code LIKE 'es%%' AND code <> %s",
        (TARGET_LANG,),
    )
    for lang_id, lang_code in env.cr.fetchall():
        env.cr.execute(
            "SELECT 1 FROM res_partner WHERE lang = %s LIMIT 1",
            (lang_code,),
        )
        if env.cr.fetchone():
            _logger.warning(
                "aries_lang_safety: %s still referenced by some partner, "
                "leaving it active.", lang_code,
            )
            continue
        env.cr.execute(
            "UPDATE res_lang SET active = FALSE WHERE id = %s",
            (lang_id,),
        )
        _logger.info("aries_lang_safety: deactivated %s", lang_code)


@_step('clear_cache')
def _clear_cache(env):
    """Invalidate ormcache so context_get rebuilds with the new partner
    langs. Wrapped in try/except because clearing during a registry
    build can occasionally surface transient issues.
    """
    env.registry.clear_cache()


def _apply_lang_safety(env):
    """Idempotent best-effort cleanup. Each step is wrapped so a failure
    in one part doesn't abort the rest — the goal is to leave the DB in
    a usable state even if one step encounters an edge case.

    Safe to run on:
    - Fresh install (post_init_hook)
    - Upgrade (migrations/<version>/post-migration.py)
    - Manual rerun from odoo-bin shell
    """
    _activate_target(env)
    _migrate_spanish(env)
    _migrate_leftover(env)
    _set_company_partners(env)
    _deactivate_non_ar_spanish(env)
    _clear_cache(env)
    _logger.info("aries_lang_safety: cleanup pass complete")


def post_init_hook(env):
    _apply_lang_safety(env)
