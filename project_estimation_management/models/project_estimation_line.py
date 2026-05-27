from odoo import api, fields, models
from odoo.exceptions import UserError


class ProjectEstimationLine(models.Model):
    _name = 'project.estimation.line'
    _description = 'Project Estimation Line'

    estimation_id = fields.Many2one('project.estimation')

    resource_type = fields.Many2one(
        'project.resource',
        string='Resource',
        required=True
    )

    hourly_cost = fields.Float("Hourly Cost")
    resource_hours = fields.Float(string='Estimated Hours')
    actual_hours = fields.Float(string='Actual Hours')
    total_hours = fields.Float(string='Calculation Hours')
    # cost_usd = fields.Float(string='Cost USD')
    cost_usd = fields.Float(
        string='Cost USD',
        compute='_compute_cost_usd',
        store=True
    )

    no_of_resources = fields.Integer(string='No. of Resources')

    price_inr = fields.Float(
        string='Price INR',
        compute='_compute_price_inr',
        store=True
    )
    remarks = fields.Text()

    @api.depends(
        'resource_hours',
        'hourly_cost',
        'no_of_resources'
    )
    def _compute_cost_usd(self):
        for rec in self:
            rec.cost_usd = (
                    rec.resource_hours *
                    rec.hourly_cost *
                    rec.no_of_resources
            )

    @api.onchange('resource_type')
    def _onchange_resource_type(self):
        for rec in self:
            rec.hourly_cost = rec.resource_type.hourly_cost

    @api.onchange('resource_hours')
    def _onchange_resource_hours(self):
        for rec in self:
            rec.cost_usd = rec.resource_hours * rec.resource_type.hourly_cost* rec.no_of_resources

    @api.depends(
        'cost_usd',
        'estimation_id.exchange_rate'
    )

    @api.depends(
        'cost_usd',
        'estimation_id.exchange_rate'
    )
    def _compute_price_inr(self):
        for rec in self:
            exchange_rate = rec.estimation_id.exchange_rate
            if exchange_rate:
                rec.price_inr = rec.cost_usd * exchange_rate
            else:
                rec.price_inr = 0



    def unlink(self):

        for rec in self:
            if rec.estimation_id.state in [
                'review',
                'approved',
                'sent',
                'cancel'
            ]:

                raise UserError(
                    'You cannot Delete estimation lines on this Status '

                )

        return super().unlink()


class ProjectResource(models.Model):
    _name = 'project.resource'
    _description = 'Project Resource Master'

    name = fields.Char(
        string='Resource Name',
        required=True
    )

    active = fields.Boolean(default=True)
    hourly_cost =fields.Float("Hourly Cost")