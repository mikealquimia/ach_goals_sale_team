# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    quotation_target = fields.Integer(
        string='Quotation Target',
        help="Target of quotations for the current month.")
    sale_target = fields.Integer(
        string='Sales Target',
        help="Target of sales for the current month.")
    invoice_target = fields.Integer(
        string='Invoice Target',
        help="Target of invoices for the current month.")
    payment_target = fields.Integer(
        string='Payments Target',
        help="Target of payment for the current month.")
    quotations_amount = fields.Float(string="Quotations amount")
    sales_amount = fields.Float(string="Sales amount")
    invoices_amount = fields.Float(string="Invoices amount")
    payments_amount = fields.Float(string="Payments amount")

    @api.multi
    def update_quotation_target(self, value):
        return self.write({'quotation_target': round(float(value or 0))})

    @api.multi
    def update_sales_amount(self, value):
        return self.write({'sales_amount': round(float(value or 0))})

    @api.multi
    def update_invoices_amount(self, value):
        return self.write({'invoices_amount': round(float(value or 0))})

    @api.multi
    def update_payments_amount(self, value):
        return self.write({'payments_amount': round(float(value or 0))})
