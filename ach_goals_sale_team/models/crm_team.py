# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    quotation_target = fields.Monetary(
        string='Quotation Target',
        help="""Target of quotations for the current month.\nRed: less than 80% of the goal.\nBlue: 80% - 99% of goal.\nGreen: 100% or more of the goal.""", currency_field='currency_id')
    sale_target = fields.Monetary(
        string='Sales Target',
        help="Target of sales for the current month.\nRed: less than 80% of the goal.\nBlue: 80% - 99% of goal.\nGreen: 100% or more of the goal.", currency_field='currency_id')
    invoice_target = fields.Monetary(
        string='Invoice Target',
        help="Target of invoices for the current month.\nRed: less than 80% of the goal.\nBlue: 80% - 99% of goal.\nGreen: 100% or more of the goal.", currency_field='currency_id')
    payment_target = fields.Monetary(
        string='Payments Target',
        help="Target of payment for the current month.\nRed: less than 80% of the goal.\nBlue: 80% - 99% of goal.\nGreen: 100% or more of the goal.", currency_field='currency_id')
    quotations_amount = fields.Monetary(string="Quotations amount", compute='_compute_quotations', currency_field='currency_id')
    sales_amount = fields.Monetary(string="Sales amount", compute='_compute_sales', currency_field='currency_id')
    invoices_amount = fields.Monetary(string="Invoices amount", compute='_compute_invoices', currency_field='currency_id')
    payments_amount = fields.Monetary(string="Payments amount", compute='_compute_payments', currency_field='currency_id')

    @api.multi
    def _compute_quotations(self):
        for rec in self:
            last_day_q = date.today().replace(day=1) + relativedelta(months=1)
            first_day_q = date.today().replace(day=1)
            query = "select sum(so.amount_total) as amount_total "
            query += "from sale_order so "
            query += "where so.state in ('draft','sent') "
            query += "and so.team_id = %s "
            query += "and so.date_order >= %s and so.date_order < %s"
            params = (rec.id, first_day_q, last_day_q)
            self.env.cr.execute(query, params)
            amount = self.env.cr.dictfetchone()
            rec.quotations_amount = amount['amount_total'] if amount else 0

    @api.multi
    def _compute_sales(self):
        for rec in self:
            last_day_q = date.today().replace(day=1) + relativedelta(months=1)
            first_day_q = date.today().replace(day=1)
            query = "select sum(so.amount_total) as amount_total "
            query += "from sale_order so "
            query += "where so.state in ('sale','done') "
            query += "and so.team_id = %s "
            query += "and so.confirmation_date >= %s and so.confirmation_date < %s"
            params = (rec.id, first_day_q, last_day_q)
            self.env.cr.execute(query, params)
            amount = self.env.cr.dictfetchone()
            rec.sales_amount = amount['amount_total'] if amount else 0

    @api.multi
    def _compute_invoices(self):
        for rec in self:
            last_day_q = date.today().replace(day=1) + relativedelta(months=1)
            first_day_q = date.today().replace(day=1)
            query = "select sum(ai.amount_total_signed) as amount_total_signed "
            query += "from account_invoice ai "
            query += "where ai.state in ('open','in_payment','paid') "
            query += "and ai.team_id = %s "
            query += "and ai.date_invoice >= %s and ai.date_invoice < %s"
            params = (rec.id, first_day_q, last_day_q)
            self.env.cr.execute(query, params)
            amount = self.env.cr.dictfetchone()
            rec.invoices_amount = amount['amount_total_signed'] if amount else 0

    @api.multi
    def _compute_payments(self):
        for rec in self:
            last_day_q = date.today().replace(day=1) + relativedelta(months=1)
            first_day_q = date.today().replace(day=1)
            query = "select sum(ap.amount) as amount "
            query += "from account_invoice ai "
            query += "inner join account_invoice_payment_rel aipr "
            query += "on aipr.invoice_id = ai.id "
            query += "inner join account_payment ap "
            query += "on ap.id = aipr.payment_id "
            query += "and ap.payment_date >= %s and ap.payment_date < %s "
            query += "where ai.team_id = %s"
            params = (first_day_q, last_day_q, rec.id)
            self.env.cr.execute(query, params)
            amount = self.env.cr.dictfetchone()
            rec.payments_amount = amount['amount'] if amount else 0
