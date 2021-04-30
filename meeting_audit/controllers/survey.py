# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from werkzeug.exceptions import NotFound
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.survey.controllers.main import Survey
import base64
from odoo.exceptions import AccessError, MissingError, UserError

from odoo.addons.portal.controllers.portal import get_records_pager, \
    pager as portal_pager, CustomerPortal


class Survey(Survey):
    # Survey start
    @http.route(['/survey/start/<model("survey.survey"):survey>',
                 '/survey/start/<model('
                 '"survey.survey"):survey>/<string:token>'],
                type='http', auth='public', website=True)
    def start_survey(self, survey, token=None, **post):
        res = super(Survey, self).start_survey(survey, token)
        return res


class CustomerPortal(CustomerPortal):

    def _get_user_input_domain(self, partner):
        return [
            ('partner_id', 'in',
             [partner.id, partner.commercial_partner_id.id]),
        ]

    def _prepare_portal_layout_values(self):
        """ Add meet details to result page """
        values = super(
            CustomerPortal, self
        )._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values['result_count'] = request.env[
            'survey.user_input'].search_count(
            self._get_user_input_domain(partner))
        return values

    def _survey_order_get_page_view_values(self, order, access_token,
                                           **kwargs):
        #
        def resize_to_48(b64source):
            if not b64source:
                b64source = base64.b64encode(Binary().placeholder())
            return image_resize_image(b64source, size=(48, 48))

        values = {
            'order': order,
            'resize_to_48': resize_to_48,
        }
        return self._get_page_view_values(order, access_token, values,
                                          'my_purchases_history',
                                          True, **kwargs)

    @http.route(['/my/result', '/my/result/page/<int:page>'],
                type='http', auth="user", website=True)
    def my_result(self, page=1, date_begin=None, date_end=None,
                  sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SurveyUserInput = request.env['survey.user_input']

        domain = self._get_user_input_domain(partner)

        archive_groups = self._get_archive_groups('survey.user_input',
                                                  domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'),
                     'result': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'result': 'name asc, id asc'}
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'new': {'label': _('New'),
                    'domain': [('state', '=', 'new')]},
            'skip': {'label': _('Skip'),
                     'domain': [('state', '=', 'skip')]},
            'done': {'label': _('Done'),
                     'domain': [('state', '=', 'done')]}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['result']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # pager
        account_count = SurveyUserInput.search_count(domain)
        pager = portal_pager(
            url="/my/result",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby},
            total=account_count,
            page=page,
            step=self._items_per_page
        )

        accounts = SurveyUserInput.search(domain, order=order,
                                          limit=self._items_per_page,
                                          offset=pager['offset'])
        request.session['my_result_history'] = accounts.ids[:100]

        values.update({
            'accounts': accounts,
            'page_name': 'result',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/result',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(
                sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("meeting_audit.portal_my_results",
                              values)

    @http.route(['/my/result/<int:account>'], type='http',
                auth="public", website=True)
    def portal_my_survey_order(self, account=None, access_token=None,
                               **kw):
        try:
            order_sudo = self._document_check_access(
                'survey.user_input', account,
                access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._survey_order_get_page_view_values(order_sudo,
                                                         access_token,
                                                         **kw)
        return request.render(
            "meeting_audit.portal_my_result_order", values)
