from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta
import re


class Patient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'
    _sql_constraints = [('Mail constrain', 'UNIQUE(email)', 'Patient email should be unique')]

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    age = fields.Integer(compute='compute_age')
    email = fields.Char()
    # related_customer_id = fields.Many2one('res.partner')
    cr_ratio = fields.Float()
    blood = fields.Selection([
        ('A', 'A'),
        ('B', 'B')
    ], default='B')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary()
    address = fields.Text()
    history = fields.Html()
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')
    department_id = fields.Many2one('hms.department')
    doctors_ids = fields.Many2many('hms.doctor', default='')
    department_capacity = fields.Integer(related='department_id.capacity')
    log_ids = fields.One2many('hms.log.hestory', 'patient_id')

    stats_dict = {
        'undetermined': 'good',
        'good': 'fair',
        'fair': 'serious',
        'serious': 'undetermined'
    }

    def change_state(self):
        self.env['hms.log.hestory'].create({
            'description': f'State changed to {self.stats_dict.get(self.state)}',
            'patient_id': self.id
        })
        self.state = self.stats_dict.get(self.state)

    @api.onchange('age')
    def on_age_change(self):
        if 0 < self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR checked',
                    'message': 'PCR has been checked'
                }
            }

    @api.constrains('email')
    def mail_constrains(self):
        if not re.search('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', self.email):
            raise UserError('Invalid Email')

    @api.depends('birth_date')
    def compute_age(self):
        if self.birth_date:
            self.age = int(relativedelta(date.today(), self.birth_date).years)
