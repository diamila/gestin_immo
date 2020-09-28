from odoo import models, fields, api, tools, exceptions, _
from datetime import datetime, timedelta

from datetime import datetime, timedelta

from odoo.addons import decimal_precision as dp
import logging


# Heritage Vente/Quittance
class Quittance(models.Model):
    _inherit = 'sale.order'  #
    
 
 
class Quittance_suite(models.Model):
    _inherit = 'sale.order' 
    
    
    
    
    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], required="True",default="service")
        
        
    #order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)    
    
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)


    
      
     
     
    
    partner_id = fields.Many2one('res.partner', string='Acheteur', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, change_default=True, index=True, track_visibility='always', track_sequence=1) 

    product_id = fields.Many2one('product.product')  
    
    
    
class order_line(models.Model):
    _inherit = 'sale.order.line'
    
    
    

    
    
    
class facture(models.Model):
    _inherit = 'account.invoice'
    
    
    type_bien = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.',related='invoice_line_ids.type_bien')
        
        
        
        
    
    #partner_id = fields.Many2one('res.partner', string='Acheteur', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, change_default=True, index=True, track_visibility='always', track_sequence=1) 

  
    
     
    paiement = fields.Selection([('mensuel', 'Mensuel'), ('bimestriel', 'Bimestriel'), ('trimestriel', 'Trimestriel'),
                                 ('semestriel', 'Semestriel'), ('annuel', 'Annuel')],
                                string="Durée Paiements")    
    
                                
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

                        
                         
    
   
   
                                
    mois_commencant = fields.Selection([('janvier', 'janvier'),
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
                                  string="mois_commençant")                             
    
    
    
    
    customer = fields.Boolean(related='partner_id.customer')
  
    
    
    
class order_uite(models.Model):
    _inherit = 'account.invoice.line'
    
    bailleur_id = fields.Many2one(related='product_id.bailleur_id', string="Bailleur")
    
    
    
    #commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='product_id.commision_bailleur')
   
    #partner_id = fields.Many2one(related='invoice_id.partner_id')
    
    #product_id = fields.Many2one('product.product', related='invoice_id.product_id')
    
    #account_id = fields.Many2one('account.account', string='Compte Agence(Dima)',  related='invoice_id.property_account_income_id')
    
    
    
    type_bien = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.', related='product_id.type')
             
             
    
    
class journal(models.Model):
    _inherit = 'account.journal' 