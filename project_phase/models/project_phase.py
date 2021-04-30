from odoo import api, fields, models, _, tools


class ProjectProject(models.Model):
    _name = 'project.project.phase'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Project Phase'
    _order = 'sequence'

    name = fields.Char(
        string='Phase name',
        translate=True,
        required=True,
        track_visibility='onchange'
    )
    code = fields.Char(
        string='Phase code'
    )
    sequence = fields.Integer(
        string='Sequence',
        deflaut=10
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env[
            'res.company'
        ]._company_default_get('project.project.type')
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    default = fields.Boolean(
        string='Default',
        default=False
    )
    note = fields.Text(
        string="Note",
        required=False
    )
    project_phase_ids = fields.Many2many(
        comodel_name="project.project",
        relation="project_phase_rel",
        column1="phase", column2="project",
        string="Phase")
