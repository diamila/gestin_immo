

# -*- coding: utf-8 -*-

from odoo import models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.maintenance'

    bien_loue = fields.Many2one('product.template', required=True)

    name = fields.Char(string="objet maintenance")




    def create_maintenance(self):
        vals = {
            'bien_loue': self.bien_loue.id,
            'name': self.name,
        }
        self.env['maintenance.request'].create(vals)


