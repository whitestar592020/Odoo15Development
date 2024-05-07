from odoo import models, fields


class Document(models.Model):
    _name = "document"
    _description = "Document"
    _table = "document"

    name = fields.Char(string="Document Name", required=True)
    file = fields.Binary(string="Document File")
    standard_cv_id = fields.Many2one(string="Related CV",
                                     comodel_name="standard.cv")
