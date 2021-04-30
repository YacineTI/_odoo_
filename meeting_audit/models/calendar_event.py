import logging

from odoo import api, fields, models, _, tools
import datetime
from werkzeug import urls
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    calendar_id = fields.Many2one(
        comodel_name='calendar.event',
        string="Calendar",
        required=False,
        reverse='id',
        index=True,
        copy=False
    )


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def _compute_is_highlighted(self):
        if self.env.context.get('active_model') == 'res.partner':
            partner_id = self.env.context.get('active_id')
            for event in self:
                if event.partner_ids.filtered(
                        lambda s:s.id == partner_id):
                    event.is_highlighted = True
                else:
                    event.is_highlighted = False
        else:
            for event in self:
                event.is_highlighted = False

    survey_result_ids = fields.One2many(
        comodel_name="survey.user_input",
        inverse_name="calendar_id",
        string="result",
        required=False
    )
    survey_id = fields.Many2one(
        comodel_name='survey.survey',
        string="Survey",
        required=False
    )
    user_input_id = fields.Many2one(
        'survey.user_input',
        string='User Input',
        required=False
    )
    state_user_input = fields.Selection(
        related='user_input_id.state',
        string='Status',
        sotre=True,
        readonly=True
    )

    public_url = fields.Char("Public link",
                             related="survey_id.public_url")
    public_url_html = fields.Char("Public link (html version)",
                                  related="survey_id.public_url_html")
    print_url = fields.Char("Print link",
                            related="survey_id.print_url")
    result_url = fields.Char("Results link",
                             related="survey_id.result_url")

    @api.multi
    def action_start_survey(self):
        """ Open the website page with the survey form """
        self.ensure_one()
        calendar_id = self.id
        if not isinstance(self.id, int):
            calendar_id = float(self.id.replace('-', '.'))
        partner_id = False
        if self.partner_ids.ids:
            partner_id = self.partner_ids.ids[0]
        response = self.env['survey.user_input'].create(
            {'survey_id':self.survey_id.id,
                'partner_id':partner_id,
                'calendar_id':int(calendar_id)})
        return self.survey_id.with_context(
            survey_token=response.token).action_start_survey()

    @api.model
    def default_get(self, fields):
        defaults = super(CalendarEvent, self).default_get(fields)
        if 'user_id' in fields:
            user = self.env['res.users'].browse(defaults['user_id'])
            defaults.update(
                {
                    'user_id':False,
                }
            )
        return defaults