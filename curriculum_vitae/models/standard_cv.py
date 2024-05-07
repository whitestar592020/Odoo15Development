from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StandardCV(models.Model):
    _name = "standard.cv"
    _description = "Standard CV"
    _table = "standard_cv"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Career Name", required=True, translate=True)
    active = fields.Boolean(default=True)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if 'name' not in default:
            default['name'] = "%s (New CV)" % self.name
        return super(StandardCV, self).copy(default=default)

    image = fields.Binary(string="Career Image")
    apply_job = fields.Many2one(string="Apply Job", comodel_name="job.type", copy=False)

    @api.onchange("apply_job")
    def _onchange_apply_job(self):
        for record in self:
            if record.apply_job:
                record.currency_id = record.apply_job.currency_id
                record.salary = record.apply_job.min_amount
                range = "{} to {}".format(record.apply_job.min_amount, record.apply_job.max_amount)
                return {'warning': {
                    'title': "Warning",
                    'message': "Salary range is between {}".format(range)
                }}

    salary = fields.Integer(string="Expect Salary", tracking=True)

    @api.constrains("salary")
    def _check_salary(self):
        for record in self:
            if record.apply_job:
                min_amount = record.apply_job.min_amount
                max_amount = record.apply_job.max_amount
                range = "{} to {}".format(min_amount, max_amount)
                if record.salary < min_amount or record.salary > max_amount:
                    raise ValidationError(
                        "Salary amount is out of range!\nIt must be between {}".format(range)
                    )

    currency_id = fields.Many2one(string="Currency Type",
                                  comodel_name="res.currency",
                                  default=lambda self: self.env.company.currency_id)
    dob = fields.Date(string="Date of Birth")
    nrc = fields.Char(string="NRC")
    nationality = fields.Char(string="Nationality")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Char(string="Current Address")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married')
    ], string="Marital Status")
    objective = fields.Text(string="Career Objectives")

    certificate_ids = fields.Many2many(string="Related Certificates",
                                       comodel_name="certificate",
                                       relation="standard_cv_certificate_rel",
                                       column1="standard_cv_id",
                                       column2="certificate_id")

    employment_line_ids = fields.One2many(string="Related Employments",
                                          comodel_name="employment.line",
                                          inverse_name="standard_cv_id")

    age_info = fields.Char(string="Career Age",
                           compute="_compute_age_info")

    @api.depends("dob", "gender")
    def _compute_age_info(self):
        for record in self:
            if record.dob:
                age = fields.Date.today().year - record.dob.year
                if record.gender == "male":
                    record.age_info = "He is {} years old".format(age)
                else:
                    record.age_info = "She is {} years old".format(age)
            else:
                record.age_info = _("Date of Birth is not set yet!")

    employment_count = fields.Integer(compute="_compute_employment_count")

    def _compute_employment_count(self):
        EmploymentLine = self.env["employment.line"]
        for record in self:
            record.employment_count = EmploymentLine.search_count([("standard_cv_id", "=", self.id)])

    document_ids = fields.One2many(comodel_name="document",
                                   inverse_name="standard_cv_id")

    def action_open_document(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Related Documents",
            "res_model": "document",
            "view_mode": "tree,form",
            "domain": [('id', 'in', self.document_ids.ids)],
            "context": {'default_standard_cv_id': self.id},
        }

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
    ], string="Status", default="draft")

    def action_draft(self):
        for record in self:
            record.state = "draft"

    def action_confirm(self):
        for record in self:
            record.state = "confirm"

    def action_done(self):
        for record in self:
            record.state = "done"

    color = fields.Integer(string="Color")
