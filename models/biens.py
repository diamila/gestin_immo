
# -*- coding: utf-8 -*-

from lxml import etree

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp



class BienNormal(models.Model):
    _inherit = 'product.product'

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'MA')], limit=1)
        return country
        
    ref = fields.Char(string="ref", default="00125")
    
    #name_a = fields.Char(string="ref", default="aaaaa")
    
    #name = fields.Char(string="name_n", compute='_fname')
    
    
    name_seq = fields.Char(string='seq', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
                           
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('bien.sequence') or _('New')
        result = super(BienNormal, self).create(vals)
        return result 
        
        
    
        
    

    latitude = fields.Char(string="Latitude", default="0.0")
    longitude = fields.Char(string="Longitude", default="0.0")
    Date = fields.Date()
    nbre_tour = fields.Integer(string="Niveau")
    ameublement = fields.Char(string="Ameublement")
    
    
    lst_price = fields.Float(related='list_price', readonly=False,
        digits=dp.get_precision('Product Price'))
    
    
    property_account_income_categ_id= fields.Many2one('account.account', company_dependent=True,
        string="Income account", oldname="property_account_income",
        domain=[('deprecated', '=', False)],
        help="Keep this field empty to use the default value from the product category.", related='categ_id.property_account_income_categ_id')
        

    expense_policy = fields.Selection(
        [('no', 'No'), ('cost', 'At cost'), ('sales_price', 'Prix')],
        string='Re-Invoice Policy',
        default='no',
        help="Expenses and vendor bills can be re-invoiced to a customer."
             "With this option, a validated expense can be re-invoice to a customer at its cost or sales price.")

    purchase_ok = fields.Boolean('Can be Purchased', default=False)

    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], string='Type de bien', default='consu', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')

   

    


    #contrat = fields.Many2one('lb.location', ondelete='cascade', string="Contrat lié au bien")




    location_ok = fields.Boolean(
        'Peut étre en location', default=True)

    type_id = fields.Many2one('lb.type', ondelete='cascade', string="Type bien")
    gestionnaire_id = fields.Many2one('lb.gestionnaire', ondelete='cascade', string="gestionnaire Immeuble", store=True)
    
    
    
    bailleur_id = fields.Many2one('lb.bailleur', string="Bailleur")
    
    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="Compte bailleur", oldname="property_account_payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        related='bailleur_id.property_account_payable_id')
        



    taux_commission = fields.Float('Taux de commission de l agence SDG(%)', default=0)

    commision_agence = fields.Float(string="Commision agence", default=5, compute='_commissionagence')

    @api.onchange('taux_commission', 'lst_price')
    def _commissionagence(self):
        for r in self:
            r.commision_agence = (r.lst_price * r.taux_commission) / 100

    commision_bailleur = fields.Float(string="Déversement bailleur", default=5, compute='_commissionbailleur')

    @api.onchange('taux_commission', 'lst_price')
    def _commissionbailleur(self):
        for r in self:
            r.commision_bailleur = (r.lst_price * (100 - r.taux_commission)) / 100

    civilite = fields.Selection([('m.', 'M.'),('mme', 'Mme'),('mlle', 'Mlle'),('m. et mme','M. et Mme')], string="Civilité", related='bailleur_id.civilite')
    num_piece_identite = fields.Char(string='Numéro de la pièce d\'identité', related='bailleur_id.num_piece_identite')
    street = fields.Char(string="Adresse1", related='bailleur_id.street')
    mobile = fields.Char(string="Mobile", related='bailleur_id.mobile')



    chambres = fields.Float(string="Nombre chambres", default=1)
    salons = fields.Float(string="Nombre salons", default=1)
    cuisines = fields.Float(string="Nombre cuisines", default=1)
    toilette = fields.Float(string="Nombre toilettes", default=1)
    cour = fields.Float(string="Espace familiale", default=1)

    salles_bain = fields.Char(string="Nombre salles de bains")
    parking = fields.Char(string="Nombre parkings")
    balcon = fields.Char(string="Nombre balcons")
    jardin = fields.Boolean(default=False, string="Jardin")
    ascenseur = fields.Boolean(default=False, string="Ascenseur")
    g_electroge = fields.Boolean(default=False, string="Groupe electrogène")


    oriente_vers = fields.Char(string="Position", default='Bordure route principale')
    # compte_revenu = fields.Many2one('lb.revenu', ondelete='cascade', string="Compte de Revenu")
    # compte_depense = fields.Many2one('ldu Bien")

    rue = fields.Char(string="Rue")

    adresse = fields.Many2one('lb.quartier', string="Quartier", required=True)

    ville = fields.Many2one('lb.ville', string="Ville")

    pays = fields.Many2one('res.country', string="Pays", default=_get_default_country)

    notes = fields.Text(string="Notes")

    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('lb.location'),
                                 index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')



    # 2 fonctions pour l'image attaché
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for bien in self:
            bien.doc_count = Attachment.search_count([('res_model', '=', 'lb.bien'), ('res_id', '=', bien.id)])

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'lb.bien'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                            Cliquez sur créer (et non importer) pour ajouter les images associées à vos biens.</p><p>
                        </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    # Calcul de la devise
    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

    # kanban: qui affiche les sessions regroupées par cours (les colonnes sont donc des cours)
    color = fields.Integer()

    # géolocalisation du bien
    def tt_locate_bien(self):
        return {
            "type": "ir.actions.act_url",
            "url": 'https://www.google.com/maps/search/?api=1&query=' + self.longitude + ', -' + self.latitude,
        }

    # champs: lien avec les information du bien
    history_ids = fields.Many2many('lb.history', string="History")
    plus_proche_ids = fields.Many2many('lb.lieu', string="Lieux plus proche")
    sous_propriete_ids = fields.Many2many('lb.sous_propriete', string="Détail des pièces")

    # champs: Plans d'étage, photos et documents
    plan_ids = fields.Many2many('lb.plan_etage', string="Plans")
    photos_ids = fields.Many2many('lb.photos', string="Photos")
    documents_ids = fields.Many2many('lb.documents', string="Documents")

   # @api.multi
    #def get_name(self):
        #for rec in self:
            #res.append((rec.nom, '%s - %s' % (prix_location)))
        #return res





    contrat_count = fields.Integer(string='Contrats', compute='get_contrat_count')

    @api.multi
    def open_bien_contrat(self):
        return {
            'name': _('Contrats'),
            'domain': [('bien_loue', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.location',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count(self):
        count = self.env['lb.location'].search_count([('bien_loue', '=', self.id)])
        self.contrat_count = count
        
        
        
    
    contrat_count_vente = fields.Integer(string='Contrats de vente', compute='get_contrat_count_vente')

    @api.multi
    def open_bien_contrat_vente(self):
        return {
            'name': _('Contrats'),
            'domain': [('bien_loue', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.contrat_vente',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count_vente(self):
        count = self.env['lb.contrat_vente'].search_count([('bien_loue', '=', self.id)])
        self.contrat_count_vente = count
        
        
    # états/barre LOCATION
    state_vente = fields.Selection([
        ('draft', 'ien disponible'),
        ('confirm', 'Bien Vendu'),
    ], compute='_onchangeEtat_vente')

    @api.onchange('bien_loue')
    def _onchangeEtat_vente(self):
        for r in self:
        # récuperer la dernier valeur du modele location et  (state)
            appointments = self.env['lb.contrat_vente'].search([('bien_loue', '=', r.id)])
            if appointments:
                for rec in appointments:
                    r.state_vente = rec.state
            
        


   # state = fields.Selection([
       # ('draft', 'New'),
        # ('confirm', 'En location'),
        # ('ferme', 'Fermé'),
    #  ], string='Status', related='etat.state')


    #open maintenance
    maintenance_count = fields.Integer(string='Maintenances', compute='get_maintenance_count')

    @api.multi
    def open_bien_maintenance(self):
        return {
            'name': _('Maintenance'),
            'domain': [('bien_loue', '=', self.id)],
            'view_type': 'form',
            'res_model': 'maintenance.request',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_maintenance_count(self):
        count = self.env['maintenance.request'].search_count([('bien_loue', '=', self.id)])
        self.maintenance_count = count

    #etat = fields.Char(compute='_onchangeEtat')
    
    etat_n = fields.Selection([
        ('draft', 'Bien Disponible'),
        ('confirm', 'Bien En location'),
        ('ferme', 'Bien Disponible'),
    ], compute='_onchangeetat_n')

    
    @api.onchange('etat')
    def _onchangeetat_n(self):
        for r in self:
            r.etat_n = r.etat
            
            

    etat = fields.Selection([
        ('draft', 'Bien Disponible'),
        ('confirm', 'Bien En location'),
        ('ferme', 'Bien Disponible'),
    ], compute='_onchangeEtat')

    @api.onchange('bien_loue')
    def _onchangeEtat(self):
        for r in self:
        # récuperer la dernier valeur du modele location et  (state)
            appointments = self.env['lb.location'].search([('bien_loue', '=', r.id)], order='id desc', limit=1)
            if appointments:
                for rec in appointments:
                    r.etat = rec.state
            else:
                r.etat = 'ferme'

    @api.multi
    def print_report(self):
        return self.env.ref('location_biens.contrat_bailleur').report_action(self)

    name_categ_id = fields.Char(related='categ_id.name', string="Catégorie du Bien")

    superficie = fields.Float('Superficie(m²)', default=0)




class Type(models.Model):
    _name = 'lb.type'
    _rec_name = 'type'

    type = fields.Char(string="Type")


class gestionnaire(models.Model):
    _name = 'lb.gestionnaire'
    _rec_name = 'gestionnaire_immeuble'

    gestionnaire_immeuble = fields.Char(string="Nom gestionnaire immeuble")




#-------------------informations
class history(models.Model):
    _name = 'lb.history'
    _rec_name = 'source'

    date = fields.Date('Date')
    source = fields.Char('Source')
    number = fields.Char('Number')

class type_lieu(models.Model):
    _name = 'lb.type_lieu'
    _rec_name = 'type_lieu'
    
  
    type_lieu = fields.Char('Type de lieu')    


class plus_proche(models.Model):
    _name = 'lb.lieu'
    _rec_name = 'name_lieu'


    name_lieu = fields.Char('Nom du lieu')
    type_lieu = fields.Many2one('lb.type_lieu', string="Type de lieu")
    distance = fields.Float(string="Distance(m)", default=5)
    
    

class sous_propriete(models.Model):
    _name = 'lb.sous_propriete'
    _rec_name = 'type_piece'


    type_piece = fields.Many2one('lb.type_piece', string="Type de pièces")
    height = fields.Float(string="longueur(m)", default=3.0)
    width = fields.Float(string="Largeur(m)", default=2.0)
    
    
class type_piece(models.Model):
    _name = 'lb.type_piece'
    _rec_name = 'type_piece'
    
  
    type_piece = fields.Char('Type de pièces')
   

class Plans_etage(models.Model):
    _name = 'lb.plan_etage'
    _rec_name = 'description_plan'


    description_plan = fields.Char('Description plan')
    photos_plan = fields.Binary(string="Photos plan", attachment=True)

class photos(models.Model):
    _name = 'lb.photos'
    _rec_name = 'description'

    description = fields.Char('Description')
    photos = fields.Binary(string="Photos", attachment=True)


class documents(models.Model):
    _name = 'lb.documents'
    _rec_name = 'description'

    description = fields.Char('Description')
    date_expiration = fields.Date('Date expiration')
    fichier = fields.Binary(string="Fichiers", attachment=True)




class Maintenance(models.Model):
    _inherit = 'maintenance.request'

    cout_maintenance = fields.Float(string="coût maintenance", default=0.0)
    bien_loue = fields.Many2one('product.product', required=True, String="Bien")




class CRM(models.Model):
    _inherit = 'crm.lead'
    
    

    type_propect = fields.Selection([('location', 'Location'), ('gerance', 'Gérance'), ('location', 'Location + Gérance')], String="Type de Prospect")

    besoin = fields.Selection(
        [('location', 'Location'), ('ach', 'Achat')],
        string="Type Besoin", related='partner_id.besoin')

    #info = fields.Char(default="veiller enregistre les modification pr que Ce prospect soit un locataire")

    active_potenctiels = fields.Selection(
        [('client', 'est un Client'), ('prospect', 'Est Un Prospect')],
        string="Statut contact", related='partner_id.active_potenctiel', default='prospect')
    #test = fields.Boolean(compute='create_locataire')

    client_type = fields.Selection(
        [('client_ache', 'Client Acheteur'), ('client_loc', 'Client Locataire')],
        string="Statut client", related='partner_id.client_type', default='client_loc')

    @api.one
    def terminer_basculer(self):
        if (self.partner_id.active_potenctiel) == 'prospect':
            self.partner_id.active_potenctiel = 'client'
            self.partner_id.client_type = 'client_loc'
            return True
        else:
            self.partner_id.active_potenctiel = 'client'
            self.partner_id.client_type = 'client_loc'

    @api.one
    def terminer_basculer_acheteur(self):
        if (self.partner_id.active_potenctiel) == 'prospect':
            self.partner_id.active_potenctiel = 'client'
            self.partner_id.client_type = 'client_ache'
            return True
        else:
            self.partner_id.active_potenctiel = 'client'
            self.partner_id.client_type = 'client_ache'




    def locataires(self):
        return {
            'name': _('Locataire'),
            'domain': [('client_type','=','client_loc'), ('active_potenctiel','=','client'), ('customer','=',True), ('parent_id', '=', False)],
            'view_type': 'form',
            'res_model': 'res.partner',
            'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }
        
    
    def acheteurs(self):
        return {
            'name': _('Acheteur'),
            'domain': [('client_type','!=','client_loc'), ('active_potenctiel','=','client'), ('customer','=',True), ('parent_id', '=', False)],
            'view_type': 'form',
            'res_model': 'res.partner',
            'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }
    




class CRM_suite(models.Model):
    _inherit = 'crm.lead'
    
    type_besoin = fields.Char(string="Besoin du prospect")
