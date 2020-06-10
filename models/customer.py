from odoo import models, fields, api
from odoo.exceptions import UserError


class Customer(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')
    vat = fields.Char(required=True)

    @api.multi
    def unlink(self):
        for record in self:
            print('record.related_patient_id========>', record.related_patient_id)
            if record.related_patient_id != False:
                raise UserError('Can not delete customer as he is linked by patient')
        super().unlink()
