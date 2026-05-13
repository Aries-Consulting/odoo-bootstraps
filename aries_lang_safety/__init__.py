# -*- coding: utf-8 -*-
import logging

import odoo.modules.registry
from odoo.http import Request

from . import models

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Monkey-patch: sanitize session.context['lang'] right after the session
# is loaded, BEFORE any ir.http override or env.lang lookup runs.
#
# Why: the ir.http._pre_dispatch override is part of the MRO chain. In
# odoo.sh "Connect" flows (or any session whose lang was set externally
# to a code that is not active in res_lang), env.lang validation can
# fire from inside auth or routing code that runs BEFORE _pre_dispatch
# reaches our override. Patching _get_session_and_dbname runs
# unconditionally on every request, before anything touches env.
#
# Failure mode: patch is best-effort. If anything raises, log it and
# return the original (unpatched) session/dbname so the request flow
# continues — never break the request because of our sanitizer.
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
                # lang is active — nothing to do
                return session, dbname
            cr.execute(_FALLBACK_SQL)
            row = cr.fetchone()
            if not row:
                # No active lang at all — leave session as-is rather
                # than guess. This shouldn't happen on a valid DB.
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
            "sess_lang=%r) — request continues with original session",
            dbname, sess_lang,
        )
    return session, dbname


Request._get_session_and_dbname = _patched_get_session_and_dbname
_logger.info("aries_lang_safety: Request._get_session_and_dbname patched")
