# -*- coding: utf-8 -*-
"""
Re-apply the language safety cleanup on every upgrade to this module.

post_init_hook only runs on first install. This migration runs on
every upgrade where the installed version is older than 18.0.1.0.1,
so improvements to _apply_lang_safety take effect without requiring a
manual uninstall + reinstall.
"""
from odoo import api, SUPERUSER_ID

from odoo.addons.aries_lang_safety.hooks import _apply_lang_safety


def migrate(cr, installed_version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_lang_safety(env)
