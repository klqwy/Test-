from odoo import fields, models


class ProjectIndustry(models.Model):
    _name = 'project.industry'
    _description = 'Project Industry'
    _rec_name = 'name'

    name = fields.Char(
        string='Industry Name',
        required=True
    )

    active = fields.Boolean(
        default=True
    )