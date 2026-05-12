# -*- coding: utf-8 -*-
"""
Re-apply the language safety cleanup on every upgrade to 18.0.1.0.2.

The 18.0.1.0.1 migration was reported failing somewhere with only
"Failed to load registry" surfacing in the build log. This version of
the cleanup logic wraps each step in try/except + traceback logging,
replaces _activate_lang with a direct SQL flip (avoiding the costly
_load_module_terms cascade), guards the leftover-lang search against
empty active_codes (which would produce SQL `NOT IN ()`), and uses
direct SQL for the deactivation step.

Re-runs even on DBs where 18.0.1.0.1 is recorded applied — fresh
version directory.
"""
from odoo import api, SUPERUSER_ID

from odoo.addons.aries_lang_safety.hooks import _apply_lang_safety


def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_lang_safety(env)
