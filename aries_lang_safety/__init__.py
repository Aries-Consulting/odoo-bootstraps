# -*- coding: utf-8 -*-
import logging

import odoo.modules.registry
from odoo.api import Environment
from odoo.http import Request
from odoo.tools import lazy_property

from . import models

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Three layers of defense, all loaded at module import:
#
# Layer 1 (this file): monkey-patch Request._get_session_and_dbname to
#   sanitize session.context['lang'] right after session load.
# Layer 2 (this file): monkey-patch Environment.lang to return a
#   graceful fallback instead of raising UserError when context.lang
#   is not active in res_lang. THIS is the bulletproof layer — it
#   intercepts the actual error site, regardless of where the bad
#   lang came from in the request lifecycle.
# Layer 3 (models/ir_http.py): override _pre_dispatch in the MRO chain
#   for sessions that bypass layer 1.
#
# Layer 2 is the one that should always work because it patches the
# exact property that raises the UserError that becomes the 400.
# ---------------------------------------------------------------------

_FALLBACK_SQL = """
    SELECT code FROM res_lang
     WHERE active
     ORDER BY CASE code
                  WHEN 'es_AR' THEN 1
                  WHEN 'en_US' THEN 2
                  ELSE 3
              END
     LIMIT 1
"""


# =====================================================================
# Layer 1: sanitize session.context['lang'] at session load time
# =====================================================================

_original_get_session_and_dbname = Request._get_session_and_dbname


def _patched_get_session_and_dbname(self):
    session, dbname = _original_get_session_and_dbname(self)
    sess_lang = session.context.get('lang') if session else None
    if not (dbname and sess_lang):
        return session, dbname
    try:
        registry = odoo.modules.registry.Registry(dbname)
        with registry.cursor() as cr:
            cr.execute(
                "SELECT 1 FROM res_lang WHERE active AND code = %s",
                (sess_lang,),
            )
            if cr.fetchone():
                return session, dbname
            cr.execute(_FALLBACK_SQL)
            row = cr.fetchone()
            if not row:
                return session, dbname
            fallback = row[0]
        session.context = dict(session.context, lang=fallback)
        session.is_dirty = True
        _logger.info(
            "aries_lang_safety: rewrote session lang %r → %r for db %s",
            sess_lang, fallback, dbname,
        )
    except Exception:
        _logger.exception(
            "aries_lang_safety: session lang sanitization failed (db=%s, "
            "sess_lang=%r)",
            dbname, sess_lang,
        )
    return session, dbname


Request._get_session_and_dbname = _patched_get_session_and_dbname
_logger.info("aries_lang_safety: Request._get_session_and_dbname patched")


# =====================================================================
# Layer 2: replace Environment.lang property — never raise on invalid
# =====================================================================

@lazy_property
def _safe_env_lang(self):
    """Replacement for Environment.lang.

    Original (odoo/api.py:765-774):
        @lazy_property
        def lang(self):
            lang = self.context.get('lang')
            if lang and lang != 'en_US' and not self['res.lang']._get_data(code=lang):
                raise UserError(f'Invalid language code: {lang}')
            return lang or None

    Replacement: when context.lang is not active in res_lang, fall back
    to the first active lang (preferring es_AR, then en_US) instead of
    raising. The UserError that becomes HTTP 400 is bypassed at its
    source.
    """
    lang = self.context.get('lang')
    if not lang or lang == 'en_US':
        return lang or None
    try:
        cr = self.cr
        cr.execute(
            "SELECT 1 FROM res_lang WHERE active AND code = %s",
            (lang,),
        )
        if cr.fetchone():
            return lang
        cr.execute(_FALLBACK_SQL)
        row = cr.fetchone()
        if row:
            _logger.debug(
                "aries_lang_safety: env.lang fallback %r → %r",
                lang, row[0],
            )
            return row[0]
        return None
    except Exception:
        _logger.exception(
            "aries_lang_safety: env.lang fallback failed for lang=%r",
            lang,
        )
        return lang or None


Environment.lang = _safe_env_lang
_logger.info("aries_lang_safety: Environment.lang patched (graceful fallback)")
