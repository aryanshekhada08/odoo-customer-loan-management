# Odoo Customer Loan Management

Customer Loan Management is an Odoo addon for managing customer loans, installments, loan documents, reminders, and loan reports.

## Features

- Create and manage customer loans
- Configure loan types
- Calculate total loan amount and EMI
- Generate loan installment lines on approval
- Track paid, partial, and unpaid installments
- Record installment payments with a payment wizard
- Send installment reminder emails with a scheduled cron job
- Attach required loan documents
- Print loan reports
- Add an Agent field and My Agent Orders filter on Sales Orders and Quotations
- Role-based access for Loan Users and Loan Admins

## Access Rules

- Loan User: can create and manage their own draft loans.
- Loan Admin: can approve, close, delete, and manage all loans, installments, loan types, documents, and payments.

## Installation

1. Copy this addon into your Odoo `custom_addons` directory.
2. Make sure `custom_addons` is included in `addons_path`.
3. Restart Odoo.
4. Update the Apps list.
5. Install or upgrade `Loan Management`.

Command example:

```bash
python odoo-bin -c odoo.conf -u customer_loan -d your_database --stop-after-init
```

## Usage

1. Open **Loan Management > Loans**.
2. Create a draft loan for a customer.
3. Login as a Loan Admin and approve the loan.
4. Odoo generates installment lines automatically.
5. Use the Pay button on an installment to record payment.

For Sales Orders and Quotations, the `Agent` field defaults to the logged-in user and the list opens with the `My Agent Orders` filter.

## Dependencies

- `base`
- `mail`
- `sale_management`
