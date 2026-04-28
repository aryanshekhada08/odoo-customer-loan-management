from odoo import models, fields


class LoanDocument(models.Model):
    _name = 'loan.document'
    _description = 'Loan Document'

    name = fields.Char(string="Document Name")