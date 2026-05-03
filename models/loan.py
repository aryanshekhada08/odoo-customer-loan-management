from odoo import models, fields, api
from odoo.exceptions import UserError
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
    user_id = fields.Many2one(
    'res.users',
    string="Assigned User",
    default=lambda self: self.env.user
    )

    def _check_loan_admin(self):
        if not self.env.user.has_group('customer_loan.group_loan_admin'):
            raise UserError("Only a Loan Admin can do this action.")

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
        self._check_loan_admin()

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
        self._check_loan_admin()
        self.state = 'done'
     
    # SEQUENCE FOR LOAN NUMBER
    @api.model_create_multi
    def create(self, vals_list):

        is_admin = self.env.user.has_group('customer_loan.group_loan_admin')
        for vals in vals_list:
            vals['document_ids'] = [(6, 0, [1,2])]
            if not is_admin:
                vals['user_id'] = self.env.user.id
                vals['state'] = 'draft'
            if vals.get('loan_no', 'New') == 'New': 
                vals['loan_no'] = self.env['ir.sequence'].next_by_code(
                    'loan.management'
                ) or 'New'
        return super().create(vals_list)

    def write(self, vals):
        is_admin = self.env.user.has_group('customer_loan.group_loan_admin')
        if not is_admin:
            blocked_fields = {'state', 'user_id', 'installment_ids'}
            if blocked_fields.intersection(vals):
                raise UserError("Only a Loan Admin can change loan status, owner, or installments.")
            if any(loan.state != 'draft' for loan in self):
                raise UserError("Only a Loan Admin can edit a loan after it is approved.")
        return super().write(vals)

    def unlink(self):
        is_admin = self.env.user.has_group('customer_loan.group_loan_admin')
        if not is_admin:
            for loan in self:
                if loan.user_id != self.env.user or loan.state != 'draft':
                    raise UserError("You can only delete your own draft loans. Approved loans must be removed by a Loan Admin.")
        return super().unlink()
    
   

         
