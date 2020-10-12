from odoo import models, fields, api, tools, exceptions, _
from datetime import datetime, timedelta

import re
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, tools, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp






#FACTURATION
class Paiement_location(models.Model):
    _name = 'lb.paiement_location'
    _rec_name = 'product_id'
    
    
    
          
    
        
    
    @api.multi
    def action_view_invoice(self):
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        form_view = [(self.env.ref('account.invoice_form').id, 'form')]
        return action
        
    contrat =fields.Many2one('lb.location', string="Contrat",  related='invoice_line_ids.product_id')      
    
    
    invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoiced')
    
    def _get_invoiced(self):
        count = self.env['sale.order'].search_count([('contrat', '=', self.id)])
        self.invoice_count = count
    
   
  
        
    @api.multi
    def action_facture(self):
        return {
            'name': _('sale_order'),
            'domain': [('contrat', '=', self.id)],
            'view_type': 'form',
            'res_model': 'sale.order',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
        
            
        
        
   
                
                
   
     
   
 
    @api.multi
    def print_facture(self):
        return self.env.ref('location_biens.facture_card_location').report_action(self)
    
    date_paiement = fields.Date(string='Date', required=True,
                                default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                

    # kanban
    color = fields.Integer()

    ref_facture = fields.Char(string="Identifiant", help="Identifiant unique de facturation")
    
    
    invoice_line_ids = fields.One2many('lb.paiement_facturation', 'paiement_id', string="Paiements")  
    
    product_id =fields.Many2one(related='invoice_line_ids.bien_loue')
     
    #bien_loue = fields.Many2one(related='invoice_line_ids.bien_loue', string="bien")
   
    
    locataire_id = fields.Many2one(related='invoice_line_ids.locataire_id', string="Locataire")
    
    partner_id = fields.Many2one(related='invoice_line_ids.partner_id', string="Locataire")
    
    mobile = fields.Char(string="N° tel locataire", related='invoice_line_ids.mobile')
    
    
    categ_id = fields.Many2one(related='invoice_line_ids.categ_id', string="catégorie du bien")
    
    
    objet_paiement = fields.Selection([('avance', 'Avance'),('loyer', 'Loyer du mois'),('autre paiements', 'Autres Paiements')]
    , string="Objet du Paiement",related='invoice_line_ids.objet_paiement')
    
    
    paiement = fields.Selection([('mensuel', 'Mensuel'), ('bimestriel', 'Bimestriel'), ('trimestriel', 'Trimestriel'),
                                 ('semestriel', 'Semestriel'), ('annuel', 'Annuel')],
                                string="Durée Paiements", related='invoice_line_ids.paiement')
    
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
                                  string="paiement du mois",  related='invoice_line_ids.mois_payee_c', attrs="{'invisible':[('paiement','!=','mensuel')]}")
                                  
                                  
                                  
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
                                  string="Mois commençant", related='invoice_line_ids.mois_commencant', attrs="{'invisible':[('paiement','=','mensuel')]}")
    
    bailleur_id = fields.Many2one(related='invoice_line_ids.bailleur_id', string="Bailleur")
    
    
    commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='invoice_line_ids.commision_bailleur')
    
    
    price_unit = fields.Float(related='invoice_line_ids.price_unit', string="Prix total")
    
    montant_location = fields.Float(related='invoice_line_ids.montant_location', string="Prix loyer/mois(sans taxe)")
    
    montant_paye = fields.Float(related='invoice_line_ids.montant_paye', string="Montant")
    
    amount_untaxed = fields.Float(related='invoice_line_ids.price_unit', string="Montant")
    

    
    property_account_income_id = fields.Many2one('account.account', company_dependent=True,
        string="Income Account", oldname="property_account_income",
        domain=[('deprecated', '=', False)],
        help="Keep this field empty to use the default value from the product category.", related='invoice_line_ids.property_account_income_id')
    
    
    
    
    
    
    
    

                            
    

#FACTURATION
class facturation_(models.Model):
    _name = 'lb.paiement_facturation'
    _rec_name = 'paiement'
    
    
    
    property_account_income_id = fields.Many2one('account.account', company_dependent=True,
        string="Income Account", oldname="property_account_income",
        domain=[('deprecated', '=', False)],
        help="Keep this field empty to use the default value from the product category.", related='product_id.property_account_income_id')
        
        
    _sql_constraints = [
        ('non_contrat_unique',
         'UNIQUE(product_id)',
         "l/'identifiant du contrat doit être unique"),
    ]        
    
    
    
    product_id =fields.Many2one('lb.location', string="Contrat associé",  domain="[('state','=','confirm')]")
    
    bien_loue = fields.Many2one(related='product_id.bien_loue', string="Bien")
    
    # états/barre LOCATION
    state = fields.Selection([
        ('draft', 'New Contrat'),
        ('confirm', 'Contrat en cour'),
        ('ferme', 'Contrat Achevé'),
    ], string='Status', related='product_id.state')   
    
    categ_id = fields.Many2one(related='product_id.categ_id', string="Catégorie du bien")
    
    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], string='Type de bien', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.',related='product_id.type')


   
    locataire_id = fields.Many2one(related='product_id.locataires', string="Locataire", store=True)
    
    partner_id = fields.Many2one(related='product_id.locataires', string="Locataire", store=True)
    
    mobile = fields.Char(string="N° Tel Locataire", related='product_id.mobile')
    
    
                                
   
 
    
    
    
   
    
    
    objet_paiement = fields.Selection([('avance', 'Avance'),('loyer', 'Loyer du mois'),('autre paiements', 'Autres Paiements')]
    , string="Objet du Paiement", default="loyer")
    
    
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
                                  string="Paiement du mois", attrs="{'invisible':[('paiement','!=','mensuel')]}")
    
    
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
                                  string="Mois commençant", attrs="{'invisible':[('paiement','=','mensuel')]}")
                                  
    
   
    
    montant_location = fields.Float(related='product_id.loyer_sans_charges', string="Prix loyer/mois")
     
   
    
    montant_paye = fields.Float(compute='_montant_paye', string="Montant payé")
    
    price_unit = fields.Float(string="Prix total", compute='_amount_total')

    @api.onchange('montant_location')
    def _amount_total(self):
        for r in self:
            r.price_unit = (r.montant_location)
            
            
   
                                
         
   
    
    
   
    
   
    
    
    @api.onchange('montant_location', 'paiement')
    def _montant_paye(self):
        for r in self:
            if (r.paiement) == 'mensuel':
                r.montant_paye = r.montant_location
            if (r.paiement) == 'bimestriel':
                r.montant_paye = r.montant_location * 2
            if (r.paiement) == 'trimestriel':
                r.montant_paye = r.montant_location * 3
            if (r.paiement) == 'semestriel':
                r.montant_paye = r.montant_location * 6
            if (r.paiement) == 'annuel':
                r.montant_paye = r.montant_location * 12   
           
    
                                        
    commentaire_paiement = fields.Text(string="Commentaire")
                                  
    
    
    commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='product_id.commision_bailleur', invisible="1")
                               
    
    bailleur_id = fields.Many2one(related='product_id.bailleur', string="Bailleur")
    
        
    
   
    
   
    
    
    paiement_id = fields.Many2one('lb.paiement_location', ondelete='cascade', string="Paiement location")