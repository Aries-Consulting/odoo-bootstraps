# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _pre_dispatch(cls, rule, args):
        # Odoo 18 sets session.context['lang'] from the browser's
        # Accept-Language header without checking it is installed
        # (odoo/http.py:_get_session_and_dbname). When the browser sends
        # `es-ES` (or just `es`, which babel aliases to es_ES) and the DB
        # only has es_AR/en_US active, env.lang raises UserError → 400.
        # Sanitize before super() so any downstream env.lang access sees
        # a valid code.
        sess_lang = request.session.context.get('lang') if request.session else None
        if sess_lang:
            cr = request.env.cr
            cr.execute(
                "SELECT 1 FROM res_lang WHERE active AND code = %s",
                (sess_lang,),
            )
            if not cr.fetchone():
                cr.execute(
                    """
                    SELECT code FROM res_lang
                     WHERE active AND code IN ('es_AR', 'en_US')
                     ORDER BY CASE code
                                  WHEN 'es_AR' THEN 1
                                  WHEN 'en_US' THEN 2
                              END
                     LIMIT 1
                    """
                )
                row = cr.fetchone()
                if not row:
                    cr.execute(
                        "SELECT code FROM res_lang WHERE active LIMIT 1"
                    )
                    row = cr.fetchone()
                fallback = row[0] if row else 'en_US'
                request.session.context = dict(
                    request.session.context, lang=fallback,
                )
                request.update_context(lang=fallback)
        super()._pre_dispatch(rule, args)
