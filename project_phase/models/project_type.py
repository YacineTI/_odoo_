from odoo import api, fields, models, _, tools


class ProjectType(models.Model):
    _name = 'project.project.type'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Project type'
    _order = 'sequence'

    name = fields.Char(
        string='Type Name',
        required=True,
        translate=True,
        track_visibility='onchange'
    )
    code = fields.Char(
        string='Code',
        default=lambda self: _('New')
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    project_id = fields.One2many(
        comodel_name='project.project',
        inverse_name='project_type_id',
        string='Project',
        copy=True,
        auto_join=True
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
    project_count = fields.Integer(
        'Job Note',
        compute='_get_project_count'
    )
    note = fields.Text(
        string="Note",
        required=False
    )

    def action_view_type(self):
        self.ensure_one()
        return {
            'name': 'Project',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'domain': [('project_type_id', '=', self.id)],
        }

    def _get_project_count(self):
        for type in self:
            project_ids = self.env['project.project'].search(
                [('project_type_id', '=', type.id)])
            type.project_count = len(project_ids)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'project.project.type') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'project.project.type') or _('New')
        result = super(ProjectType, self).create(vals)
        return result
