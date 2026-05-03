from datetime import timedelta
from unittest.mock import patch

from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLoanEmails(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'Email Test Customer',
            'email': 'customer@example.com',
        })
        cls.loan_type = cls.env['loan.type'].create({
            'name': 'Email Test Loan',
        })
        cls.loan = cls.env['loan.management'].create({
            'customer_id': cls.customer.id,
            'loan_type_id': cls.loan_type.id,
            'amount': 1000.0,
            'interest': 0.0,
            'duration': 1,
        })
        cls.installment = cls.env['loan.installment'].create({
            'loan_id': cls.loan.id,
            'sequence': 1,
            'amount': 1000.0,
            'due_date': fields.Date.today() + timedelta(days=1),
        })

    def test_payment_template_creates_mail(self):
        mail_ids = self.installment._send_payment_received_email(force_send=False)
        self.assertTrue(mail_ids)
        mail = self.env['mail.mail'].browse(mail_ids[0])
        self.assertIn(self.loan.loan_no, mail.subject)

    def test_reminder_template_creates_mail(self):
        mail_ids = self.installment._send_reminder_email(force_send=False)
        self.assertTrue(mail_ids)
        mail = self.env['mail.mail'].browse(mail_ids[0])
        self.assertIn('Reminder', mail.subject)

    def test_payment_wizard_sends_payment_email(self):
        wizard = self.env['loan.payment.wizard'].create({
            'installment_id': self.installment.id,
            'amount': 1000.0,
        })
        with patch.object(
            type(self.env['loan.installment']),
            '_send_payment_received_email',
            return_value=[1],
        ) as send_email:
            wizard.action_confirm_payment()
        self.assertEqual(self.installment.state, 'paid')
        send_email.assert_called_once()
