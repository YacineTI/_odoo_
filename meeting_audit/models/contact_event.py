from odoo import api, fields, models, _, tools


class ContactEvent(models.Model):
    _inherit = 'res.partner'

    calendar_ids = fields.Many2many(
        comodel_name="calendar.event",
        inverse_name="calendar_event_res_partner_rel",
        string="Meeting",
        required=False
    )