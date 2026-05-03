from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one(
        'res.users',
        string="Agent",
        default=lambda self: self.env.user,
        tracking=True
    )
