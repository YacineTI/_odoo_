# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from werkzeug.exceptions import NotFound
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import json
from odoo.addons.portal.controllers.portal import get_records_pager, \
    pager as portal_pager, CustomerPortal


class CustomerPortal(CustomerPortal):

    def _get_meet_domain(self, partner):
        return [
            ('partner_ids', 'in',
             [partner.id, partner.commercial_partner_id.id]),
        ]

    def _prepare_portal_layout_values(self):
        """ Add meet details to main page """
        values = super(CustomerPortal,
                       self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values['meet_count'] = request.env[
            'calendar.event'].search_count(
            self._get_meet_domain(partner))
        return values

    @http.route(['/my/meet', '/my/meet/page/<int:page>'], type='http',
                auth="user", website=True)
    def my_meet(self, page=1, date_begin=None, date_end=None,
                sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        CalendarEvent = request.env['calendar.event']

        domain = self._get_meet_domain(partner)

        archive_groups = self._get_archive_groups('calendar.event',
                                                  domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'),
                     'meet': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'meet': 'name asc, id asc'}
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'open': {'label': _('In Progress'),
                     'domain': [('state', '=', 'open')]}
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['meet']
        # default filter by value
        if not filterby:
            filterby = 'open'
        domain += searchbar_filters[filterby]['domain']

        # pager
        account_count = CalendarEvent.search_count(domain)
        pager = portal_pager(
            url="/my/meet",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby},
            total=account_count,
            page=page,
            step=self._items_per_page
        )

        accounts = CalendarEvent.search(domain, order=order,
                                        limit=self._items_per_page,
                                        offset=pager['offset'])
        request.session['my_meet_history'] = accounts.ids[:100]

        values.update({
            'accounts': accounts,
            'page_name': 'meet',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/meet',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(
                sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("meeting_audit.portal_my_meets",
                              values)

    @http.route(['/my/meets/create/<string:calendar_id>'],
                type='http', auth="user", website=True)
    def my_meet_create(self, calendar_id, **post):
        calendar = request.env['calendar.event'].browse(calendar_id)
        partner_id = False
        if calendar.partner_ids.ids:
            partner_id = calendar.partner_ids.ids[0]
        response = request.env['survey.user_input'].create(
            {'survey_id': calendar.survey_id.id,
             'partner_id': partner_id, 'calendar_id': calendar_id})
        # ret = {'redirect': '/survey/fill/%s/%s' % (calendar.survey_id.id, response.token)}
        # return calendar.survey_id.with_context(survey_token=response.token).public_url
        # return json.dumps(ret)
        return request.redirect('/survey/fill/%s/%s' % (
            calendar.survey_id.id, response.token))
