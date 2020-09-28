from odoo import models, fields, api, tools, exceptions, _
from datetime import datetime, timedelta

from datetime import datetime, timedelta

from odoo.addons import decimal_precision as dp
import logging


# Heritage Vente/Quittance
class Quittance(models.Model):
    _inherit = 'sale.order'  #
    
 
 
class Quittance_suite(models.Model):
    _inherit = 'sale.order'  #
    
    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], required="True",default="service")
        
class order_line(models.Model):
    _inherit = 'sale.order.line'
    

    
    
    
    
class facture(models.Model):
    _inherit = 'account.invoice'
    
    partner_id = fields.Many2one('res.partner', string='Acheteur', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, change_default=True, index=True, track_visibility='always', track_sequence=1) 

  
    product_id = fields.Many2one('product.template')   
    
    
    
    price_unit = fields.Float(string='Prix')

          



    
    
    
    
                                       


class order(models.Model):
    _inherit = 'account.invoice.line'

     
    partner_id = fields.Many2one(related='invoice_id.partner_id')
    
    product_id = fields.Many2one('product.template', related='invoice_id.product_id')
    
    price_unit = fields.Float(related='invoice_id.price_unit')
    
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
        ondelete='cascade', index=True)

    
    
    bailleur_id = fields.Many2one(related='product_id.bailleur_id', string="Bailleur")

    commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='product_id.commision_bailleur')


    commision_agence = fields.Float(string="Commision agence", default=5, related='product_id.commision_agence')
    
    mois_payee_c = fields.Selection([('janvier', 'janvier'),
                                   ('fevrier', 'février'),
                                   ('mars', 'mars'),
                                   ('avril', 'avril'),
                                   ('mai', 'mai'),
                                   ('juin', 'juin'),
                                   ('juillet', 'juillet'),
                                   ('aout', 'août'),
                                   ('septembre', 'septembre'),
                                   ('octobre', 'octobre'),
                                   ('novembre', 'novembre'),
                                   ('decembre', 'décembre')],
                                  string="paiement du mois")
    
    
    

    