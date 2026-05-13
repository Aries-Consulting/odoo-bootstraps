# -*- coding: utf-8 -*-
"""
Aries Language Safety — minimal v3.0.0

Single intervention: replace `Environment.lang` to return a fallback
instead of raising `UserError` when `context.lang` is not active in
`res_lang`.

Why this is the only patch we need:

The original `Environment.lang` at `odoo/api.py:765` raises
`UserError(f'Invalid language code: {lang}')`. Odoo's HTTP dispatcher
catches that UserError and converts it to a `BadRequest` 400 response.
Every code path that produces the `Invalid language code: es_ES` 400
ends at this single property access. Patching this property is the
only intervention guaranteed to run regardless of where in the request
lifecycle a bad lang was injected — which previously included odoo.sh
"Connect" flows that bypassed session-level and `_pre_dispatch`-level
defenses.

Earlier versions tried multiple defensive layers (a session sanitizer
on `Request._get_session_and_dbname`, an `ir.http._pre_dispatch`
override, post_init hooks that activated `es_AR` and migrated users).
All of them were positional — they could be bypassed by specific code
paths. This patch is at the actual raise site.

Risk:
Any Odoo code that depends on `env.lang` raising `UserError` for an
invalid lang code (instead of falling back) would no longer detect
the misconfiguration. In production this is exactly the behavior we
want — the misconfiguration was the symptom, not a state we need to
surface.

Fallback priority: `es_AR`, then `en_US`, then any other active lang,
then `None`.
"""
import logging

from odoo.api import Environment
from odoo.tools import lazy_property

_logger = logging.getLogger(__name__)


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


def lang(self):
    """Replacement for Environment.lang — see module docstring.

    Named `lang` (not e.g. `_safe_env_lang`) so `lazy_property` caches
    the result under the correct attribute name on the env instance.
    """
    requested = self.context.get('lang')
    if not requested or requested == 'en_US':
        return requested or None
    try:
        cr = self.cr
        cr.execute(
            "SELECT 1 FROM res_lang WHERE active AND code = %s",
            (requested,),
        )
        if cr.fetchone():
            return requested
        cr.execute(_FALLBACK_SQL)
        row = cr.fetchone()
        if row:
            _logger.debug(
                "aries_lang_safety: env.lang fallback %r → %r",
                requested, row[0],
            )
            return row[0]
        return None
    except Exception:
        _logger.exception(
            "aries_lang_safety: env.lang fallback failed for lang=%r",
            requested,
        )
        return requested or None


Environment.lang = lazy_property(lang)
_logger.info("aries_lang_safety v3.0.0: Environment.lang patched")
