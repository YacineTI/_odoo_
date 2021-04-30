from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError

AVAILABLE_PRIORITIES = [
    ('0', 'New'),
]


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # @api.model
    # def _compute_state(self):
    #     AVAILABLE_PRIORITIES = [
    #         ('0', 'New'),
    #     ]
    #     obj_phase = self.env['project.project.phase']
    #     phase_id = obj_phase.search(
    #         [])
    #     for project in phase_id:
    #         seq = str(project.sequence)
    #         name = project.name
    #         state = (seq, name)
    #         AVAILABLE_PRIORITIES.extend([(state)])
    #     return AVAILABLE_PRIORITIES

    project_type_id = fields.Many2one(
        comodel_name='project.project.type',
        string="Project type",
        required=False
    )

    project_phase_ids = fields.Many2many(
        comodel_name="project.project.phase",
        relation="project_phase_rel",
        column1="project", column2="phase",
        string="Phase line"
    )
    # 9
    phase_id = fields.Many2one(
        'project.project.phase',
        string='Phase',
        ondelete='restrict',
        track_visibility='onchange',
        index=True,
        copy=False,
        default=lambda self: self._default_phase_id()
    )

    def _default_phase_id(self):
        return self._phase_find().id

    def _phase_find(self, domain=None,
                    order='sequence'):
        search_domain = []
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env['project.project.phase'].search(search_domain,
                                                        order=order,
                                                        limit=1)

    def project_left(self):
        for project in self:
            if not project.project_phase_ids:
                return

            phase = project.phase_id.name
            mylist = project.project_phase_ids.mapped('name')

            if phase not in mylist:
                return

            li = mylist.index(phase)
            if li <= 0:
                ref = self.env.ref(
                    'project_phase.project_project_phase').id
                project.sudo().write({'phase_id': ref})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

            old = mylist[li - 1]
            list_phase = project.project_phase_ids.filtered(
                lambda r: r.name == old
            )
            project.sudo().write({'phase_id': list_phase.id})

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def project_right(self):
        for project in self:
            if not project.project_phase_ids:
                return
            phase = project.phase_id.name
            mylist = project.project_phase_ids.mapped('name')

            if phase not in mylist:
                newid = project.project_phase_ids[0]
                project.sudo().write({'phase_id': newid.id})
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

            li = mylist.index(phase)
            if li + 1 >= len(mylist):
                return

            next = mylist[li + 1]
            list_phase = project.project_phase_ids.filtered(
                lambda r: r.name == next
            )
            project.sudo().write({'phase_id': list_phase.id})

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    # @api.onchange('phase_id')
    # def _onchange_phase_id(self):
    # if self.phase_id.name != 'New' and self.phase_id not in \
    # self.project_phase_ids:
    # raise UserError(_(
    # 'This phase does not exist in the project.'))
