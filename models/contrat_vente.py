# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, tools, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp

from datetime import datetime, timedelta


class ContratVente(models.Model):
    _name = 'lb.contrat_vente'
    _rec_name = 'contrat_id'
    
    contrat_id = fields.Char(string="Ref contrat", compute='_contrat_locataire_bien')
    
   
            
            
    
    @api.multi
    def action_facture_vente(self):
        for rec in self:
            rec.state_f = 'invoiced'
        return {
            'name': _('sale_order'),
            'view_type': 'form',
            'res_model': 'sale.order',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }
        
        
    contrat_count_vente = fields.Integer(string='facture', compute='get_contrat_count_facture')


    def get_contrat_count_facture(self):
        count = self.env['sale.order']
        self.contrat_count_vente = count
    
        
        

    date = fields.Date(string='Date', required=True,
                                default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    
    
    name_locataire = fields.Char(string="name locataire", related='locataires.name')
    
    name_bien = fields.Char(string="name bien", related='bien_loue.name')
    
    @api.onchange('name_locataire','name_bien')
    def _contrat_locataire_bien(self):
        for r in self:
            r.contrat_id = r.name_locataire + '/' + r.name_bien
            
            
            

    _sql_constraints = [
        ('non_contrat_unique',
         'UNIQUE(contrat_id)',
         "l/'identifiant du contrat doit être unique"),
    ]

    # champs---Information BIen"
    bien_loue = fields.Many2one('product.product', string="Bien vendu")
    
    
     # états/barre LOCATION
    product_id = fields.Many2one('product.product', string="Bien vendu", compute='_onchangebien')

    @api.onchange('bien_loue')
    def _onchangebien(self):
        for r in self:
            r.product_id = r.bien_loue
            
            
   
    
   
    
                        
                    
                    

    _sql_constraints = [
        ('non-bien_unique',
         'UNIQUE(bien_loue)',
         "Bien deja vendu"),
    ]

    standard_price = fields.Float(related='bien_loue.standard_price')




    bailleur = fields.Many2one(related='bien_loue.bailleur_id', string="Propriétaire Bien vendu")

    civilite = fields.Selection([('m.', 'Monsieur'), ('mme', 'Madame'), ('mlle', 'Mademoiselle'), ('m. et mme', 'M. et Mme')],
                                string="Civilité", related='bailleur.civilite')

    nbre_tour = fields.Integer(string="Niveau", related='bien_loue.nbre_tour')

    type_bien = fields.Many2one(related='bien_loue.type_id', string="Type de bien")

    categ_id = fields.Many2one(related='bien_loue.categ_id', string="Catégorie bien")

    adresse = fields.Many2one(related='bien_loue.adresse', string="Adresse du bien")

    ville = fields.Many2one(related='bien_loue.ville', string="Ville")
    rue = fields.Char(related='bien_loue.rue',string="Rue")

    chambres = fields.Float(related='bien_loue.chambres')
    salons = fields.Float(related='bien_loue.salons')
    cuisines = fields.Float(related='bien_loue.cuisines')
    toilette = fields.Float(related='bien_loue.toilette')
    cour = fields.Float(related='bien_loue.cour')

    salles_bain = fields.Char(related='bien_loue.salles_bain')
    parking = fields.Char(related='bien_loue.parking')
    balcon = fields.Char(related='bien_loue.balcon')

    jardin = fields.Boolean(related='bien_loue.jardin')
    ascenseur = fields.Boolean(related='bien_loue.ascenseur')
    g_electroge = fields.Boolean(related='bien_loue.g_electroge')


    prixlocation_id = fields.Float(string="Prix de Vente",
                                   related='bien_loue.list_price', default=0.0)



   
    # champs----locataire
    
    
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="Acheteur", compute='_onchangepartner')

    @api.onchange('locataires')
    def _onchangepartner(self):
        for r in self:
            r.partner_id = r.locataires
            
            
    locataires = fields.Many2one('res.partner', ondelete='cascade', string="Acheteur")
    mobile = fields.Char(string="N° Tel Acheteur", related='locataires.phone')
    adresse_locataire = fields.Char(string="Adresse acheteur",
                                    related='locataires.street')

    title = fields.Many2one(related='locataires.title')
    cin_ou_passeport = fields.Char(string="CIN ou passeport n°",
                                   related='locataires.num_piece_identite')


    #
    loyer_sans_charges = fields.Float(string="Prix de vente en fcfa", related='bien_loue.list_price', default=0.0,
                                      digits=dp.get_precision('Prix de Vente hors charges'))
    frais_retard = fields.Float(string='Frais de retard (%)', default=0.0,
                                digits=dp.get_precision('Frais de retard (%)'))
    autre_paiement = fields.Float(string='Autre Paiements', digits=dp.get_precision('Autre Paiements'))
    description_autre_paiement = fields.Text(string="Autre paiements : Description")
    enregistrement_paiement = fields.One2many('lb.paiement', 'paiement_id', string="Paiements")
    condition_particuliere = fields.Text(string="Conditions")
    reste_a_payer = fields.Float(string="Reste à payer", default=0.0, digits=dp.get_precision('Reste à Payer'))
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('lb.contrat_vente'),
                                 index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")
    locataire_a_jour = fields.Selection([('oui', 'Oui'), ('non', 'Non')], string="Le locataire est-il à jour ?")



    # états/barre LOCATION
    state = fields.Selection([
        ('draft', 'New Contrat'),
        ('confirm', 'Contrat Bien Vendu'),
    ], string='Status', readonly=True, default='confirm')
    
    
    state_f = fields.Selection([("settled", "A Facturer"),
                   ("invoiced", "Facturé")], string="Etat facture", readonly=True, default="settled")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            self.depot_retourne = False

    def action_done(self):
        for rec in self:
            rec.state = 'draft'
            self.depot_retourne = False


            # Calcul du loyer

            # Statut Location


    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

            # Contrat attaché

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for bien in self:
            bien.doc_count = Attachment.search_count([('res_model', '=', 'lb.contrat_vente'), ('res_id', '=', bien.id)])

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'lb.contrat_vente'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Cliquez sur Créer (et non importer) pour ajouter vos contrats de Vente</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    color = fields.Integer()

    @api.multi
    def print_report_vente(self):
        return self.env.ref('location_biens.contrat_card_vente').report_action(self)



    #courtier
    courtier = fields.Many2one('lb.courtier_vente')

    taux_commission_courtier = fields.Float('taux de commission courtier(%)')



    mobile = fields.Char(string="Mobile acheteur", related='courtier.mobile')

    active_commision = fields.Boolean('active_courtier vente', default=False)
    commision_courtier = fields.Float(string="Commision courtier", default=0.0, compute='_commissioncourtier')

    @api.onchange('prixlocation_id','active_commision','taux_commission_courtier')
    def _commissioncourtier(self):
        for r in self:
            if r.active_commision == True:
                r.commision_courtier = (r.prixlocation_id * r.taux_commission_courtier) / 100
            else:
                r.commision_courtier = 0



    #agence
    commision_agence = fields.Float(string="Commision agence", related='bien_loue.commision_agence')

    commision_agence_net = fields.Float(string="Commision agence net", compute='_commissionagence_net')

    @api.onchange('commision_agence', 'active_commision')
    def _commissionagence_net(self):
        for r in self:
            if r.active_commision == True:
                if r.commision_agence != 0:
                    r.commision_agence_net = (r.commision_agence - r.commision_courtier)
                else:
                    r.commision_agence_net = r.commision_agence 
            
    #bailleur
    commision_bailleur = fields.Float(string="Déversement bailleur", related='bien_loue.commision_bailleur')
    
    commision_bailleur_net = fields.Float(string="Déversement bailleur net", compute='_commission_bailleur_net')
    
    
    
    @api.onchange('commision_bailleur', 'active_commision','commision_agence_net','commision_courtier')
    def _commission_bailleur_net(self):
        for r in self:
            if r.active_commision == True:
                if r.commision_agence_net == 0:
                    r.commision_bailleur_net = r.commision_bailleur - r.commision_courtier
                else:
                    r.commision_bailleur_net = r.commision_bailleur
           





class Courtier_vente(models.Model):
    _name = 'lb.courtier_vente'
    _rec_name = 'nom_courtier'

    nom_courtier = fields.Char(string="Nom du Courtier")

    civilite = fields.Selection([('m.', 'M.'), ('mme', 'Mme'), ('mlle', 'Mlle'), ('m. et mme', 'M. et Mme')],
                                string="Civilité")
    email = fields.Char(string="E-mail", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    street = fields.Char(string="Adresse")
    ville = fields.Char(string="Ville")

    num_piece_identite = fields.Char(string='Numéro de la pièce d\'identité')

    contrat_count_vente = fields.Integer(string='Contrats', compute='get_contrat_count_vente')

    @api.multi
    def open_courtier_contrat_vente(self):
        return {
            'name': _('Contrats'),
            'domain': [('courtier', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.contrat_vente',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count_vente(self):
        count = self.env['lb.contrat_vente'].search_count([('courtier', '=', self.id)])
        self.contrat_count_vente = count
