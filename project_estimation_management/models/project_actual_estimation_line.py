from odoo import api, fields, models


class ProjectActualEstimationLine(models.Model):
    _name = 'project.actual.estimation.line'
    _description = 'Project Actual Estimation Line'

    estimation_id = fields.Many2one(
        'project.estimation',
        string='Estimation'
    )

    resource_type_id = fields.Many2one(
        'project.resource',
        string='Resource',
        required=True
    )

    hourly_cost = fields.Float(
        string='Hourly Cost'
    )

    actual_hours = fields.Float(
        string='Actual Hours'
    )

    cost_usd = fields.Float(
        string='Cost USD',
        compute='_compute_cost',
        store=True
    )

    price_inr = fields.Float(
        string='Price INR',
        compute='_compute_price_inr',
        store=True
    )

    remarks = fields.Text()

    @api.onchange('resource_type_id')
    def _onchange_resource(self):

        for rec in self:

            rec.hourly_cost = (
                rec.resource_type_id.hourly_cost
            )

    @api.depends('actual_hours', 'hourly_cost')
    def _compute_cost(self):

        for rec in self:

            rec.cost_usd = (
                rec.actual_hours *
                rec.hourly_cost
            )

    @api.depends(
        'cost_usd',
        'estimation_id.exchange_rate'
    )
    def _compute_price_inr(self):

        for rec in self:

            if rec.estimation_id.exchange_rate:

                rec.price_inr = (
                    rec.cost_usd *
                    rec.estimation_id.exchange_rate
                )

            else:

                rec.price_inr = 0