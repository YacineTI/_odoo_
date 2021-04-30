# -*- coding: utf-8 -*-
# © 2020 Osis

from odoo import api, models, fields, _


class ResRegion(models.Model):
    _name = "res.region"
    _description = "Country region"

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        return super(ResRegion, self).copy(default)

    country_id = fields.Many2one(
        'res.country',
        string='Country',
        required=True
    )
    name = fields.Char(
        string="Region",
        required=True
    )
    image_url = fields.Binary(
        related="country_id.image",
        string="Flag Image",
        store=True
    )

    _sql_constraints = [

        ('region_country_id_unique', 'unique(country_id, name)',
         'Region must be unique by Country'),
    ]
