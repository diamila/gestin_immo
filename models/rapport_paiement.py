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
    
    
    contrat =fields.Many2one('lb.location', string="Contrat") 
  
    contrat_id = fields.Char(string="Ref contrat")
    
    _sql_constraints = [
        ('non_contrat_unique',
         'UNIQUE(contrat_id)',
         "Vous avez déjà créé une facture de vente pour ce contrat"),
    ]        
    
    
    
    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à louer')], required="True",related='product_id.type')
        
        
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
        ('service', 'Bien à louer')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.',related='invoice_line_ids.type_bien')
        
        
        
        
    
    #partner_id = fields.Many2one('res.partner', string='Acheteur', states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, change_default=True, index=True, track_visibility='always', track_sequence=1) 

  
    
     
      
    
                                
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

                        
                         
    
   
   
                                
  
    
    
    
    customer = fields.Boolean(related='partner_id.customer')
    
    supplier = fields.Boolean(related='partner_id.supplier')
    
    agent = fields.Boolean(related='partner_id.agent')
    
class facture_suite(models.Model):
    _inherit = 'account.invoice'    
    
   
    

    
    product = fields.Many2one('product.product', related="invoice_line_ids.product_id") 
    
    
    
    
    
    customer = fields.Boolean(related='partner_id.customer')
    supplier = fields.Boolean(related='partner_id.supplier')
    
  
    
   
    
    date_debut = fields.Date(string='Date debut', required=True,
                                default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                
    date_to =  fields.Date(string="Date fin", store=True,
        compute='_get_end_date')

    
    
    duration = fields.Float(default=34, help="Duration in days")

    @api.depends('date_debut', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.date_debut and r.duration):
                r.date_to = r.date_debut
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.date_to = r.date_debut + duration
            
            
            
class facture_suite_suite(models.Model):
    _inherit = 'account.invoice'    
    
    contrat =fields.Many2one('lb.location', string="Contrat")   
    
    line_n = fields.One2many(
        comodel_name="sale.commission.settlement.line",
        inverse_name="settlement", string="Lignes de règlement")
        
        
        
    invoice_l = fields.Many2one(related='line_n.invoice_line')  
    
    product_id = fields.Many2one(related='line_n.product_id') 
    
class order_uite(models.Model):
    _inherit = 'account.invoice.line'
    
    bailleur_id = fields.Many2one(related='product_id.bailleur_id', string="Bailleur")
    
    
    
    #commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='product_id.commision_bailleur')
   
    #partner_id = fields.Many2one(related='invoice_id.partner_id')
    
    #product_id = fields.Many2one('product.product', related='invoice_id.product_id')
    
    #account_id = fields.Many2one('account.account', string='Compte Agence(Dima)',  related='invoice_id.property_account_income_id')
    
    
    
    type_bien = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à louer')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.', related='product_id.type')
             
             
             
             
             
             
             
    
    
class journal(models.Model):
    _inherit = 'account.journal' 
    

    
    
    
class commission_settlement(models.Model):
    _inherit = "sale.commission.settlement"
    
    
    product = fields.Many2one(related='lines.product_id')
    
    
    state = fields.Selection(
        selection=[("settled", "A Déverser"),
                   ("invoiced", "Déverser"),
                   ("cancel", "Annulé"),
                   ("except_invoice", "Exception des déversements")], string="State", readonly=True, default="settled")
        
        
        
    
class commission_settlement_suite(models.Model):
    _inherit = "sale.commission.settlement"
    
   
  
           
    lines = fields.One2many(
        comodel_name="sale.commission.settlement.line",
        inverse_name="settlement", string="Lignes de règlement", readonly=True)
        
        
    line_n = fields.One2many(
        comodel_name="sale.commission.settlement.line",
        inverse_name="settlement", string="Lignes de règlement", compute='_onchangeline')
        
        
        
    
        
    @api.onchange('lines')
    def _onchangeline(self):
        for r in self:
            r.line_n = r.lines           
                
    
    
    agent_line = fields.Many2many(
        comodel_name='account.invoice.line.agent',
        relation='settlement_agent_line_rel', column1='settlement_id',
        column2='agent_line_id', required=True)
    
    invoice_line = fields.Many2one(
        comodel_name='product.product', store=True,
        related='agent_line.object_id', string="produit")
        
        
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="bailleir/courtier", compute='_onchangepartner')

    @api.onchange('agent')
    def _onchangepartner(self):
        for r in self:
            r.partner_id = r.agent    
    
    
        
    @api.multi
    def action_facture(self):
        return {
            'name': _('facture'),
            'view_type': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context': {'settlement_ids': self.ids}
        }
        
    

class SettlementLine(models.Model):
    _inherit = "sale.commission.settlement.line"
    
  
    product_id = fields.Many2one(
        comodel_name='product.product', store=True,
        related='agent_line.product_id') 
        
class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"
   
    
    product_id = fields.Many2one(
        comodel_name='product.product', store=True,
        related='object_id.product_id') 

    