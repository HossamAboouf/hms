from odoo import models, fields, api


class LogHestory(models.Model):
    _name = 'hms.log.hestory'

    # created_by = fields.Char()
    created_by = fields.Many2one('res.users')
    date = fields.Datetime()
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')

    @api.model
    def create(self, val):
        new_log = super().create(val)
        new_log.date = new_log.create_date
        return new_log
