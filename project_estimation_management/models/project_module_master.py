from odoo import api, fields, models

from odoo import fields, models


class ProjectModuleMaster(models.Model):
    _name = 'project.module.master'
    _description = 'Modules Master'
    _rec_name = 'name'

    name = fields.Char(string='Module', required=True)
    description = fields.Text(string='Description')
    module_cost = fields.Float(string='Module Cost')
    active = fields.Boolean(default=True)