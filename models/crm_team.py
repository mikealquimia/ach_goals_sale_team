# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    quotation_target = fields.Float(
        string='Quotation Target',
        help="Target of quotations for the current month.")
    sale_target = fields.Float(
        string='Sales Target',
        help="Target of sales for the current month.")
    invoice_target = fields.Float(
        string='Invoice Target',
        help="Target of invoices for the current month.")
    payment_target = fields.Float(
        string='Payments Target',
        help="Target of payment for the current month.")
    quotations_amount = fields.Float(string="Quotations amount", compute='_compute_quotations')
    sales_amount = fields.Float(string="Sales amount", compute='_compute_sales')
    invoices_amount = fields.Float(string="Invoices amount", compute='_compute_invoices')
    payments_amount = fields.Float(string="Payments amount", compute='_compute_payments')

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

    @api.multi
    def _compute_quotations(self):
        next_month = date.today().replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        first_day = date.today().replace(day=1)
        for rec in self:
            quotation_data = self.env['sale.order'].search([
                ('state', 'in', ['draft','sent']),
                ('team_id', '=', rec.id),
                ('date_order', '<=', last_day),
                ('date_order', '>=', first_day),
            ])
            amount_team = 0
            for quota in quotation_data:
                amount_team += quota.amount_total
            rec.quotations_amount = amount_team

    @api.multi
    def _compute_sales(self):
        next_month = date.today().replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        first_day = date.today().replace(day=1)
        for rec in self:
            sale_data = self.env['sale.order'].search([
                ('state', 'in', ['sale','done']),
                ('team_id', '=', rec.id),
                ('confirmation_date', '<=', last_day),
                ('confirmation_date', '>=', first_day),
            ])
            amount_team = 0
            for sale in sale_data:
                amount_team += sale.amount_total
            rec.sales_amount = amount_team

    @api.multi
    def _compute_invoices(self):
        next_month = date.today().replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        first_day = date.today().replace(day=1)
        for rec in self:
            invoice_data = self.env['account.invoice'].search([
                ('state', 'in', ['open','in_payment','paid']),
                ('team_id', '=', rec.id),
                ('date_invoice', '<=', last_day),
                ('date_invoice', '>=', first_day),
            ])
            amount_team = 0
            for invoice in invoice_data:
                amount_team += invoice.amount_total_signed
            rec.invoices_amount = amount_team

    @api.multi
    def _compute_payments(self):
        next_month = date.today().replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)
        first_day = date.today().replace(day=1)
        for rec in self:
            invoice_data = self.env['account.invoice'].search([
                ('state', 'in', ['open','in_payment','paid']),
                ('team_id', '=', rec.id),
                ('date_invoice', '<=', last_day),
                ('date_invoice', '>=', first_day),
            ])
            amount_team = 0
            for invoice in invoice_data:
                for payment in invoice.payment_ids:
                    amount_team += payment.amount
            rec.payments_amount = amount_team
