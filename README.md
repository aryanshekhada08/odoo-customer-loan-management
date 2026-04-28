# Customer Loan Management - Odoo 19 Module

A custom Odoo 19 module for managing customer loans, installments, payments, and loan tracking with dynamic installment payment logic.

---

# Features

## Loan Management
- Create customer loans
- Auto-generated loan numbers
- Loan approval workflow
- Loan closing functionality
- Loan state tracking

---

## Installment Management
- Automatic installment generation
- EMI calculation
- Due date tracking
- Installment payment tracking
- Partial payment support
- Extra payment handling
- Dynamic due amount updates

---

## Dynamic Payment System
### Supported Payment Types
- Exact installment payment
- Partial payment
- Extra payment
- Full loan repayment

### Smart Logic
- Extra payment automatically adjusts next installments
- Paid amount tracking
- Due amount tracking
- Auto installment state updates

---

## Payment Wizard
- Popup payment wizard
- Auto-filled due amount
- Payment date selection
- Payment method support
- Notes section

---

## Email Notifications
- Installment payment email notifications
- Dynamic email templates
- Customer payment confirmation mails

---

## Reporting
- Printable loan reports
- Installment details
- Customer loan summary
- PDF report generation using QWeb

---

# Technologies Used

- Odoo 19
- Python
- PostgreSQL
- XML
- QWeb Reports

---

# Module Structure

```bash
customer_loan/
│
├── models/
│   ├── loan.py
│   ├── loan_installment.py
│   ├── loan_document.py
│   └── loan_type.py
│
├── wizard/
│   ├── payment_wizard.py
│   └── payment_wizard_view.xml
│
├── views/
│   └── loan_views.xml
│
├── reports/
│   ├── loan_report.xml
│   └── loan_report_template.xml
│
├── data/
│   ├── sequence.xml
│   └── mail_template.xml
│
├── security/
│   └── ir.model.access.csv
│
└── __manifest__.py
