from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class LoanManagement(models.Model):
    _name = 'loan.management'
    _description = 'Loan Management'

    # BASIC
    loan_type_id = fields.Many2one(
        'loan.type',
        string="Loan Type",
        required=True
    )
    customer_id = fields.Many2one(
        'res.partner',
        string="Customer",
        required=True
    )

    loan_type_id = fields.Many2one(
        'loan.type',
        string="Loan Type"
    )

    amount = fields.Float(string="Loan Amount", required=True)

    interest = fields.Float(string="Interest (%)")

    duration = fields.Integer(string="Duration (Months)")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done')
    ], default='draft')

    # COMPUTE
    total_amount = fields.Float(
        string="Total Amount",
        compute="_compute_total_amount",
        store=True
    )

    emi = fields.Float(
        string="EMI",
        compute="_compute_emi",
        store=True
    )
    document_ids = fields.Many2many(
        'loan.document',
        string="Documents",
    )
    # RELATED FIELDS
    street = fields.Char(
        related='customer_id.street',
        store=True
    )

    city = fields.Char(
        related='customer_id.city',
        store=True
    )

    zip = fields.Char(
        related='customer_id.zip',
        store=True
    )

    state_id = fields.Many2one(
        related='customer_id.state_id',
        comodel_name='res.country.state',
        store=True
    )

    country_id = fields.Many2one(
        related='customer_id.country_id',
        comodel_name='res.country',
        store=True
    )

    # INSTALLMENTS
    installment_ids = fields.One2many(
        'loan.installment',
        'loan_id',
        string="Installments"
    )
    loan_no = fields.Char(
        string="Loan Number",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )

    # TOTAL
    @api.depends('amount', 'interest')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount + (
                rec.amount * rec.interest / 100
            )

    # EMI
    @api.depends('total_amount', 'duration')
    def _compute_emi(self):
        for rec in self:
            if rec.duration:
                rec.emi = rec.total_amount / rec.duration
            else:
                rec.emi = 0
    
    # @api.model
    # def default_get(self, fields):
    #     res = super().default_get(fields)
    #     res['document_ids'] = [(6, 0, [1,2])]
    #     return res
    
    
    # APPROVE
    def action_approve(self):

        for rec in self:

            rec.state = 'running'

            rec.installment_ids.unlink()

            for i in range(rec.duration):

                self.env['loan.installment'].create({
                    'loan_id': rec.id,
                    'sequence': i + 1,
                    'amount': rec.emi,
                    'due_date': date.today() + relativedelta(months=i + 1),
                    'state': 'unpaid',
                })

    # CLOSE
    def action_mark_paid(self):
        self.state = 'done'
     
    # SEQUENCE FOR LOAN NUMBER
    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            vals['document_ids'] = [(6, 0, [1,2])]
            if vals.get('loan_no', 'New') == 'New': 
                vals['loan_no'] = self.env['ir.sequence'].next_by_code(
                    'loan.management'
                ) or 'New'
        return super().create(vals_list)
    
   

         
