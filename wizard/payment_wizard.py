from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class LoanPaymentWizard(models.TransientModel):

    _name = 'loan.payment.wizard'
    _description = 'Loan Payment Wizard'

    installment_id = fields.Many2one('loan.installment',string="Installment")
    amount = fields.Float( string="Amount")
    payment_date = fields.Date(
        string="Payment Date",
        default=fields.Date.today )
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer')
    ], string="Payment Method")
    note = fields.Text(string="Notes")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get(
            'active_id'
        ) or self.env.context.get('default_installment_id')
        installment = self.env[
            'loan.installment'
        ].browse(active_id)
        if installment:
            res['installment_id'] = installment.id
            res['amount'] = installment.due_amount
        return res

    def action_confirm_payment(self):
        if not self.env.user.has_group('customer_loan.group_loan_admin'):
            raise UserError("Only a Loan Admin can confirm payments.")

        installment = self.installment_id
        payment_amount = self.amount

        if not installment:
            raise ValidationError("Please select an installment.")
        if payment_amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

        current_due = installment.due_amount
       
        if payment_amount == current_due:
            installment.write({
                'paid_amount':
                    installment.paid_amount + payment_amount,
                'due_amount': 0,
                'state': 'paid',
                'payment_date': self.payment_date,
            })

        elif payment_amount > current_due:
            extra_amount = payment_amount - current_due

            # current installment fully paid
            installment.write({
                'paid_amount':
                    installment.paid_amount + current_due,
                'due_amount': 0,
                'state': 'paid',
                'payment_date': self.payment_date,
            })
            next_installments = self.env[
                'loan.installment'
            ].search([
                ('loan_id', '=', installment.loan_id.id),
                ('state', '!=', 'paid'),
                ('id', '!=', installment.id),
            ], order='due_date asc')
            remaining_extra = extra_amount

            for next_inst in next_installments:
                if remaining_extra <= 0:
                    break

                # FULL NEXT INSTALLMENT PAID
                if remaining_extra >= next_inst.due_amount:
                    remaining_extra -= next_inst.due_amount

                    next_inst.write({
                        'paid_amount':
                            next_inst.amount,
                        'due_amount': 0,
                        'state': 'paid',
                        'payment_date': self.payment_date,
                    })

                # PARTIAL NEXT INSTALLMENT
                else:
                    new_paid = (
                        next_inst.paid_amount
                        + remaining_extra
                    )
                    new_due = (
                        next_inst.due_amount
                        - remaining_extra
                    )
                    next_inst.write({
                        'paid_amount': new_paid,
                        'due_amount': new_due,
                        'state': 'partial',
                    })
                    remaining_extra = 0

        else:
            new_paid = (
                installment.paid_amount
                + payment_amount
            )
            new_due = (
                installment.due_amount
                - payment_amount
            )
            installment.write({

                'paid_amount': new_paid,

                'due_amount': new_due,

                'state': 'partial',
            })


    
        # template = self.env.ref(
        #     'customer_loan.email_template_installment_paid'
        # )
        # mail_id = template.send_mail(
        #     self.installment_id.id,
        #     # force_send=True
        # )
        # return {
        #     'type': 'ir.actions.act_window_close'
        # }
