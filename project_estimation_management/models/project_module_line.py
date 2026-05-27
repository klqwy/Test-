from odoo import api, fields, models


class ProjectEstimationModuleLine(models.Model):
    _name = 'project.estimation.module.line'
    _description = 'Project Estimation Module Line'

    estimation_id = fields.Many2one(
        'project.estimation',
        string='Estimation'
    )

    module_id = fields.Many2one(
        'project.module.master',
        string='Module',
        required=True
    )

    description = fields.Text(
        string='Description',
        related='module_id.description',
        store=True
    )

    module_cost = fields.Float(
        string='Cost'
    )

    @api.onchange('module_id')
    def _onchange_module_id(self):
        for rec in self:
            rec.module_cost = rec.module_id.module_cost