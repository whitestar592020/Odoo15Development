from odoo import models, fields


class Employment(models.Model):
    _name = "employment"
    _description = "Employment"
    _table = "employment"

    name = fields.Char(string="Job Position", required=True)
    company = fields.Char(string="Company")


class EmploymentLine(models.Model):
    _name = "employment.line"
    _description = "Employment Line"
    _table = "employment_line"

    employment_id = fields.Many2one(string="Job Position",
                                    comodel_name="employment")
    company = fields.Char(string="Company",
                          related="employment_id.company")
    responsibility = fields.Char(string="Responsibility")
    period_from = fields.Date(string="Period From")
    period_to = fields.Date(string="Period To")

    standard_cv_id = fields.Many2one(string="Related CV",
                                     comodel_name="standard.cv")
