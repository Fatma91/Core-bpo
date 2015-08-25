from openerp import models, fields

class partner(models.Model):
    _inherit='res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.sessions',string="Attended Sessions", readonly=True)
