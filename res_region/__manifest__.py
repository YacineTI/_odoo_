# -*- coding: utf-8 -*-
# © 2020 Osis

{
    'name': 'Partner region',
    'version': '13.0.0.1',
    'category': 'Partner',
    'summary': 'Add partner region',
    'author': 'Osis',
    'website': 'https://www.osis.dz',
    'license': 'OPL-1',
    'depends': [
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_region_views.xml',
        'views/res_partner_views.xml',
    ],

    'qweb': [],
    'images': ['static/description/icon_.png'],
    'installable': True,
    'application': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
