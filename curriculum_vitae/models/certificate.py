from odoo import models, fields


class Certificate(models.Model):
    _name = "certificate"
    _description = "Certificate"
    _table = "certificate"

    name = fields.Char(string="Certificate", required=True)
    education_center = fields.Char(string="Education Center")
