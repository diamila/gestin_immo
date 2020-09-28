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


        
class order_line(models.Model):
    _inherit = 'sale.order.line'
    
    
    
    
  
    
    
    
class facture(models.Model):
    _inherit = 'account.invoice'
    
    
  
     
     
    
    partner_id = fields.Many2one('res.partner', string='Acheteur', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, change_default=True, index=True, track_visibility='always', track_sequence=1) 

  
   
    
   
    
    
    
    price_unit = fields.Float(string='montant payé sans taxe')

          
    
    
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
                                  string="paiement du mois", attrs="{'invisible':[('paiement','!=','mensuel')]}")

class facture_suite(models.Model):
    _inherit = 'account.invoice'
    
    
    type_bien = fields.Selection([
        ('vendre', 'bien à vendre'),
        ('location', 'Bien à loué')])
        
        
    montant_location = fields.Float(string="prix loyer/mois")    
    
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
                                  string="mois_commençant", attrs="{'invisible':[('paiement','=','mensuel')]}") 
    
    
    
    
class facture_suite_suite(models.Model):
    _inherit = 'account.invoice'
    
    bien_loue = fields.Many2one('product.product')   
    
    
    invoice_line_ids = fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines', oldname='invoice_line',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    
    
    bailleur_id = fields.Many2one(related='invoice_line_ids.bailleur_id', string="Bailleur")

    commision_bailleur = fields.Float(string="Déversement bailleur", default=5, related='invoice_line_ids.commision_bailleur')


    #commision_agence = fields.Float(string="Commision agence", default=5, related='product_id.commision_agence')
    
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="compte Payable", oldname="property_account_payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        related='invoice_line_ids.property_account_payable_id')
        

    account_id = fields.Many2one('account.account', string='Compte Agence(Dima)',  related='invoice_line_ids.account_id')
    
    
    
        

class order(models.Model):
    _inherit = 'account.invoice.line'

     
    partner_id = fields.Many2one(related='invoice_id.partner_id')
    
   
    product_id = fields.Many2one('product.product', related='invoice_id.bien_loue')
    
    
    bailleur_id = fields.Many2one(related='product_id.bailleur_id', string="Bailleur")

    commision_bailleur = fields.Float(string="Déversement bailleur", default=5, related='product_id.commision_bailleur')


    #commision_agence = fields.Float(string="Commision agence", default=5, related='product_id.commision_agence')
    
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="compte Payable", oldname="property_account_payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        related='product_id.property_account_payable_id')
        
    
    
    #price_unit = fields.Float(related='invoice_id.price_unit')
    
    invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',
        ondelete='cascade', index=True)
        
        
        
   
        
  
    
    
    
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
    
    
    
    
     
    
class account_move(models.Model):
    _inherit = 'account.move'
    

    commision_bailleur = fields.Float(string="Déversement bailleur")


    #commision_agence = fields.Float(string="Commision agence", default=5, related='product_id.commision_agence')
    
    property_account_payable_id = fields.Many2one('account.account', string='Compte bailleur(credit)')
    
    
        

    account_id = fields.Many2one('account.account', string='Compte Agence"Dima"(debit)')
    
    
      
    
class account_move_line(models.Model):
    _inherit = 'account.move.line'
    
    
    line_ids = fields.One2many('account.move.line', 'move_id', string='Journal Items',
        states={'posted': [('readonly', True)]}, copy=True)
        
    move_id = fields.Many2one('account.move', string='Journal Entry', ondelete="cascade",
        help="The move of this entry line.", index=True, required=True, auto_join=True)    
   
    account_id = fields.Many2one('account.account', string='Account', related='move_id.property_account_payable_id')
    
    #debit = fields.Monetary(default=0.0, related='move_id.account_id')
    
    #debit = fields.Many2one(related='move_id.commision_bailleur')
        
   
    #account_id = fields.Many2one(related='line_ids.account_id', string='Compte Agence"Dima"(debit)')
    
       

    