from odoo import api, fields, models
from odoo.exceptions import UserError


class ProjectEstimation(models.Model):
    _name = 'project.estimation'
    _description = 'Project Estimation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    module_line_ids = fields.One2many(
        'project.estimation.module.line',
        'estimation_id',
        string='Module Costing'
    )

    total_module_cost = fields.Float(
        string='Total Module Cost',
        compute='_compute_total_module_cost',
        store=True
    )



    industry_id = fields.Many2one('project.industry',string='Industry')
    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer',required=True)
    project_name = fields.Char(string='Project Name',required=True,tracking=True)
    project_type = fields.Selection([
        ('odoo', 'Odoo'),
        ('mobile_app', 'Mobile App'),
        ('custom_build', 'Custom Build'),
        ('other', 'Other')
    ], string='Project Type',required=True)

    estimation_date = fields.Date(default=fields.Date.today)
    quoted_amount = fields.Float(
        string='Quoted Amount(INR)',

        store=True,
        copy=False
    )

    quoted_amount_usd = fields.Float(
        string='Quoted Amount (in USD)',
        compute='_compute_quoted_amount_usd',
        store=True,copy=False
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Reviewed'),
        ('approved', 'Approved'),
        ('sent', 'Sent'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True, copy=False)

    line_ids = fields.One2many(
        'project.estimation.line',
        'estimation_id',
        string='Estimation Lines'
    )

    total_hours = fields.Float(
        compute='_compute_totals',
        store=True
    )

    total_price_inr = fields.Float(string="Total Planned Effort Cost(INR)",

                                   store=True
                                   )

    profitability = fields.Float(
        string='Profitability(%)',
        compute='_compute_profitability',
        store=True,
        copy=False
    )
    actual_line_ids = fields.One2many(
        'project.actual.estimation.line',
        'estimation_id',
        string='Actual Estimation Lines'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.ref('base.USD')
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        default=lambda self: self.env.company.currency_id
    )

    exchange_rate = fields.Float(
        string='Exchange Rate (USD)',
        compute='_compute_exchange_rate',
        store=True
    )
    profit_percentage = fields.Float(
        string="Profit percentage"
    )

    @api.depends(
        'total_price_inr',
        'profit_percentage'
    )
    def _compute_quoted_amount(self):

        for rec in self:
            rec.quoted_amount = (
                    rec.total_price_inr +
                    (
                            rec.total_price_inr *
                            rec.profit_percentage / 100
                    )
            )

    @api.depends('module_line_ids.module_cost')
    def _compute_total_module_cost(self):
        for rec in self:
            rec.total_module_cost = sum(
                rec.module_line_ids.mapped('module_cost')
            )

    @api.depends('currency_id')
    def _compute_exchange_rate(self):

        for rec in self:

            if rec.currency_id:

                rec.exchange_rate = rec.currency_id._get_conversion_rate(
                    rec.currency_id,
                    rec.company_currency_id,
                    self.env.company,
                    rec.estimation_date or fields.Date.today()
                )

            else:

                rec.exchange_rate = 1

    def unlink(self):
        if not self.env.user.has_group('base.group_system'):
            raise UserError(
                'Only Administrators can delete estimations.'
            )
        return super().unlink()


    @api.depends(
        'quoted_amount',
        'exchange_rate'
    )
    def _compute_quoted_amount_usd(self):

        for rec in self:

            if rec.exchange_rate:

                rec.quoted_amount_usd = (
                        rec.quoted_amount /
                        rec.exchange_rate
                )

            else:

                rec.quoted_amount_usd = 0


    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'project.estimation'
                ) or 'New'

        records = super().create(vals_list)

        return records


    @api.depends('line_ids.price_inr', 'line_ids.resource_hours')
    def _compute_totals(self):
        for rec in self:
            rec.total_hours = sum(rec.line_ids.mapped('resource_hours'))
            rec.total_price_inr = sum(rec.line_ids.mapped('price_inr'))





    @api.depends(
        'quoted_amount',
        'total_price_inr',
        'profit_percentage',
        'line_ids.price_inr'
    )


    @api.depends(
        'line_ids.price_inr',
        'line_ids.resource_hours',
        'profit_percentage'
    )
    def _compute_profitability(self):

        for rec in self:

            total_price = sum(rec.line_ids.mapped('price_inr'))

            quoted_amount = (
                    total_price +
                    (total_price * rec.profit_percentage / 100)
            )

            rec.total_price_inr = total_price
            rec.quoted_amount = quoted_amount

            if quoted_amount:
                rec.profitability = (
                                            (quoted_amount - total_price)
                                            / quoted_amount
                                    ) * 100
            else:
                rec.profitability = 0







    def action_review(self):
        self.state = 'review'

    def action_approve(self):
        self.state = 'approved'

    def action_send(self):
        self.state = 'sent'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_to_draft(self):

        self.state = 'draft'


