from . import loan
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

class LoanInstallment(models.Model):
    _name = 'loan.installment'

    loan_id = fields.Many2one('loan.management', ondelete='cascade')
    sequence = fields.Integer()
    due_date = fields.Date()
    amount = fields.Float()
    paid_amount = fields.Float( string='Paid Amount',  default=0)
    due_amount = fields.Float(string='Due Amount')
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid')
    ], default='unpaid')

    payment_date = fields.Date()

    def _has_customer_email(self):
        self.ensure_one()
        return bool(self.loan_id.customer_id.email)

    def _send_payment_received_email(self, force_send=True):
        template = self.env.ref(
            'customer_loan.email_template_installment_paid',
            raise_if_not_found=False,
        )
        if not template:
            return False
        mail_ids = []
        for installment in self:
            if not installment._has_customer_email():
                continue
            mail_ids.append(template.send_mail(
                installment.id,
                force_send=force_send,
                email_layout_xmlid='mail.mail_notification_light',
            ))
        return mail_ids

    def _send_reminder_email(self, force_send=True):
        template = self.env.ref(
            'customer_loan.email_template_installment_reminder',
            raise_if_not_found=False,
        )
        if not template:
            return False
        mail_ids = []
        for installment in self:
            if not installment._has_customer_email():
                continue
            mail_ids.append(template.send_mail(
                installment.id,
                force_send=force_send,
                email_layout_xmlid='mail.mail_notification_light',
            ))
        return mail_ids

    def action_pay(self):
        if not self.env.user.has_group('customer_loan.group_loan_admin'):
            raise UserError("Only a Loan Admin can record installment payments.")
        return {
            'name': 'Pay Installment',
            'type': 'ir.actions.act_window',
            'res_model': 'loan.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_installment_id': self.id,
                'default_amount': self.amount,
            }
        }
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'amount' in vals:
                vals['due_amount'] = vals['amount']
        return super().create(vals_list)

    @api.model
    def cron_send_installment_reminder(self):
        tomorrow = fields.Date.today() + timedelta(days=1)
        installments = self.search([
            ('due_date', '=', tomorrow),
            ('state', '!=', 'paid')
        ])
        installments._send_reminder_email(force_send=True)
        return True
