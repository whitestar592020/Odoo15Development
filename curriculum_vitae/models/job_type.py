from odoo import models, fields


class JobType(models.Model):
    _name = "job.type"
    _description = "Job Type"
    _table = "job_type"

    name = fields.Char(string="Job Type", required=True)
    description = fields.Text(string="Description")

    currency_id = fields.Many2one(string="Currency Type", comodel_name="res.currency")
    min_amount = fields.Monetary(string="Minimum Amount")
    max_amount = fields.Monetary(string="Maximum Amount")

    cv_ids = fields.One2many(string="Related CVs",
                             comodel_name="standard.cv",
                             inverse_name="apply_job")
