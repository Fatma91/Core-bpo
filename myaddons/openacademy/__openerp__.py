# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",
    'version': '1.0',
    'author': "core-bpo",
    'website': "http://www.core-bpo.com",
    'summary': """ openacademy module """,
    'description': """ openacabemy module for manage training:
                       - training sessions
                       - training courses """,

    'depends': ['base'],
    'data':[
        'security/openacademy_security.xml',
        'security/ir.model.access.csv',
        'openacademy_view.xml',
        'partner_view.xml',
    ],
}