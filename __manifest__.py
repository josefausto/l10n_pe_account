# -*- coding: utf-8 -*-
{
    'name': "Peruvian accounting",

    'summary': """
        Account, CPE, PLE""",

    'description': """
        Peruvian accounting
    """,

    'author': "Grupo YACCK",
    'website': "http://www.grupoyacck.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'l10n_pe_cpe', 'document', 'report_xlsx'],

    # always loaded
    'data': [
        'data/pe.datas.csv',
        'security/pe_account_security.xml',
        'security/ir.model.access.csv',
        'views/pe_account_config_view.xml',
        'views/country_view.xml',
    ],
}