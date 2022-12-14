# -*- coding: utf-8 -*-
{
    'name': "Travel Umroh",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PT. Ismata Nusantara Abadi",
    'website': "https://ismata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'report_xlsx'],

    # always loaded
    'data': [
        'report/report_invoice.xml',
        'report/report_delivery.xml',
        'report/report_action.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    # Set menjadi aplikasi
    'application': True,
}
