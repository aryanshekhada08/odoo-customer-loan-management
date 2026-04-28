from odoo import models,fields,api

class loan_type(models.Model):
    _name='loan.type'
    _description = "Loan Type "

    name = fields.Char(string="Loan Name", required=True)