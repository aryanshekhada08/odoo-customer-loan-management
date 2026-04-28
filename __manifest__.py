{
    'name': 'Loan Management',
    'version': '1.0',
    'summary': 'Manage loans, members, repayments and fines',
    'author': 'Aryan',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/payment_wizard_view.xml',
        'data/mail_template.xml', 
        'reports/loan_report.xml',
        'reports/loan_report_template.xml',
        'views/loan_views.xml',
    ],
    'installable': True,
    'application': True,
}
