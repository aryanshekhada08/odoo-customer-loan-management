# Odoo Customer Loan Management

An Odoo 19 addon for managing customer loans, installment schedules, payment tracking, email reminders, PDF reports, and salesperson/agent filtering on Sales Orders.

This module was built as a practical business workflow addon, not just a UI demo. It includes role-based security, automated installment generation, payment validation, scheduled reminders, QWeb reporting, and Odoo test cases for the email flow.

## Highlights

- Loan lifecycle: Draft -> Running -> Done
- EMI and total amount calculation
- Automatic installment generation on loan approval
- Partial, full, and advance installment payment handling
- Payment wizard for controlled installment collection
- Customer payment confirmation emails
- Scheduled email reminders for installments due tomorrow
- PDF loan report using QWeb
- Loan document and loan type master data
- Two-level access control: Loan User and Loan Admin
- Sales Order inheritance with Agent field
- Default `My Agent Orders` filter on Sales Orders and Quotations
- Odoo test cases for mail template and payment email behavior

## Business Flow

1. A Loan User creates a draft loan for a customer.
2. A Loan Admin reviews and approves the loan.
3. The system generates installment lines based on duration and EMI.
4. A Loan Admin records payment from the installment payment wizard.
5. The customer receives a payment confirmation email.
6. The daily cron sends reminder emails for installments due tomorrow.
7. Admin can print the loan PDF report.

## Access Control

The module includes a simple, practical security setup:

| Role | Access |
| --- | --- |
| Loan User | Create and manage own draft loans, read own installments |
| Loan Admin | Manage all loans, installments, loan types, documents, payments, approval, closing, and deletion |

Rules are enforced in both XML security files and Python methods. Admin-only actions such as approving loans, closing loans, and recording payments are protected server-side.

## Features

### Loan Management

- Customer and loan type selection
- Loan amount, interest, and duration
- Computed total amount
- Computed EMI
- Loan number sequence
- Assigned user tracking
- Customer address fields from partner
- Document tagging

### Installment Management

- Installments are generated automatically on approval
- Due dates are calculated month by month
- Payment states: Unpaid, Partial, Paid
- Due amount and paid amount tracking
- Advance payment support across next installments

### Email Automation

- Payment received email after confirming payment
- Reminder email for installments due tomorrow
- Cron job: `Send Installment Reminder`
- Templates use Odoo 19 QWeb/Jinja syntax
- Recipients come from the loan customer partner

### Sales Order Agent Filter

This addon also extends Sales Orders:

- Adds `Agent` field on `sale.order`
- Defaults agent to the logged-in user
- Adds `My Agent Orders` search filter
- Applies this filter by default on Sales Orders and Quotations

## Technical Stack

- Odoo 19
- Python models and business methods
- XML views, actions, security, cron, and mail templates
- QWeb PDF report
- Odoo record rules and ACL security
- Odoo `TransactionCase` tests

## Installation

Clone or copy this addon into your custom addons path:

```bash
custom_addons/customer_loan
```

Make sure your `odoo.conf` contains your custom addons directory:

```ini
addons_path = /path/to/odoo/addons,/path/to/custom_addons
```

Update the apps list, then install or upgrade the module:

```bash
python odoo-bin -c odoo.conf -d your_database -u customer_loan --stop-after-init
```

## Configuration

1. Go to **Settings > Users & Companies > Users**.
2. Assign users to one of these roles:
   - `Loan Management / Loan User`
   - `Loan Management / Loan Admin`
3. Configure the outgoing mail server in Odoo for real email delivery.
4. Make sure customers have an email address on their contact record.

## Testing

Run the module tests:

```bash
python odoo-bin -c odoo.conf -d your_database -u customer_loan --test-enable --test-tags /customer_loan --stop-after-init
```

Current tested result:

```text
3 email tests passed
0 failures
0 errors
```

The tests cover:

- Payment email template creates an outgoing mail record
- Reminder email template creates an outgoing mail record
- Payment wizard calls the payment email flow

## Project Structure

```text
customer_loan/
+-- data/
|   +-- cron_jobs.xml
|   +-- email_template.xml
|   +-- mail_template.xml
|   +-- sequence.xml
+-- models/
|   +-- document.py
|   +-- loan.py
|   +-- loan_installment.py
|   +-- loan_type.py
|   +-- sale_order.py
+-- reports/
|   +-- loan_report.xml
|   +-- loan_report_template.xml
+-- security/
|   +-- groups.xml
|   +-- ir.model.access.csv
|   +-- loan_rules.xml
+-- tests/
|   +-- test_email.py
+-- views/
|   +-- loan_views.xml
|   +-- sale_order_action.xml
|   +-- sale_order_search_view.xml
|   +-- sale_order_view.xml
+-- wizard/
    +-- payment_wizard.py
    +-- payment_wizard_view.xml
```

## Main Models

| Model | Purpose |
| --- | --- |
| `loan.management` | Main loan record |
| `loan.installment` | Installment schedule and payment state |
| `loan.type` | Loan type master |
| `loan.document` | Required loan documents |
| `loan.payment.wizard` | Installment payment wizard |
| `sale.order` | Extended with Agent field |

## Notes

- Real inbox delivery depends on Odoo outgoing mail server settings.
- Existing old records may need an assigned customer email to receive messages.
- The `My Agent Orders` filter only shows orders where `agent_id` is the logged-in user.

## Author

Aryan
