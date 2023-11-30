# -*- coding: utf-8 -*-
{
    'name': 'Customer Payment Detailed  Report',
    'version': '14.0',
    'summary': 'Customer Payment Detailed Report',
    'sequence': 10,
    'category': '',
    'description': 'Customer Payment Detailed Report',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/customer_payment_wizard.xml',
        'report/pdf_report.xml',
        'report/customer_payment_pdf_template.xml'
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
