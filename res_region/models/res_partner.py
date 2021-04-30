# -*- coding: utf-8 -*-
# © 2020 Osis

from odoo import api, models, fields


class ResParter(models.Model):
    _inherit = 'res.partner'

    region_id = fields.Many2one(
        "res.region",
        string="Region",
        ondelete="set null"
    )