# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp


class Locataire(models.Model):
    _inherit = 'res.partner'

    type_piece_identite = fields.Selection([('cni', 'Carte national d\'identité'),('carte_sejour', 'Carte de séjour'),('passport', 'Passport')],string='Type de la pièce d\'identité')
    num_piece_identite = fields.Char(string='Numéro de la pièce d\'identité')
    ville = fields.Char()
    type = fields.Selection([('contact', 'Contact')], string='Address Type', help="Used to select automatically the right address according to the context in sales and purchases documents.")
    ville = fields.Char()
    enregistrement_contact = fields.One2many('lb.contact', 'contact_id', string="Contact")

    
class Contact(models.Model):
    _name = 'lb.contact'

    contact_id = fields.Many2one('res.partner', ondelete='cascade', string="Contact")
    nom_contact = fields.Char(string="Nom du Contact", required=True)
    telephone_contact = fields.Char(string="Téléphone", required=True)
    email_contact = fields.Char(string="E-mail")
    notes_contact = fields.Text(string="Notes")




