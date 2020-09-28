# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, tools, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo.osv import expression
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp

from datetime import datetime, timedelta

from odoo.exceptions import ValidationError


class Location(models.Model):
    _name = 'lb.location'
    _rec_name = 'contrat_id'
    
    
    @api.multi
    def new_contrat(self):
        return {
            'name': _('Maintenance'),
            'view_type': 'form',
            'res_model': 'lb.location',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }
        

    date = fields.Date(string='Date', required=True,
                                default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    contrat_id = fields.Char(string="ref contrat", required=True)

    _sql_constraints = [
        ('non_contrat_unique',
         'UNIQUE(contrat_id)',
         "l/'identifiant du contrat doit être unique"),
    ]
    
    
    _sql_constraints = [
        ('name_description_check',
         'UNIQUE(etat_bien != confirm)',
         "The title of the course should not be the description"),
    ]


    
    

    superficie = fields.Float('Superficie(m²)', related='bien_loue.superficie')
    

    # champs---Information BIen"
    bien_loue = fields.Many2one('product.product', string="Bien Loué")
    
    
   
    
    property_account_income_id = fields.Many2one('account.account', company_dependent=True,
        string="Income Account", oldname="property_account_income",
        domain=[('deprecated', '=', False)],
        help="Keep this field empty to use the default value from the product category.", related='bien_loue.property_account_income_id')
        
    
    commision_bailleur = fields.Float(string="Commision bailleur", default=5, related='bien_loue.commision_bailleur')

    standard_price = fields.Float(related='bien_loue.standard_price')
    
    type = fields.Selection([
        ('consu', 'bien à vendre'),
        ('service', 'Bien à loué')], string='Product Type', default='service', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.',related='bien_loue.type')


    etat_n = fields.Selection([
        ('draft', 'Bien Disponible'),
        ('confirm', 'Bien En location'),
        ('ferme', 'Bien Disponible'),
    ],related='bien_loue.etat_n')

    #state qui es lié au bien
    etat_bien = fields.Selection([
        ('draft', 'Disponible'),
        ('confirm', 'Bien En location'),
        ('ferme', 'Bien Disponible'),
    ],related='bien_loue.etat')

    @api.onchange('etat_bien')
    def _check_etat_bien(self):
        if (self.etat_bien) == 'confirm':
            return {
                'warning': {
                    'title': "Ce bien est en location",
                    'message': "Veuillez choisir un autre bien svp",
                },
            }
            
    

    
    
    @api.constrains('nbre_tour')
    def _check_debut_fin_bail(self):
        for r in self:
            if r.nbre_tour > 1:
                raise exceptions.ValidationError("La fin du bail doit être supérieur au début du bail")
                
    


    bailleur = fields.Many2one(related='bien_loue.bailleur_id', string="Bailleur")

    civilite = fields.Selection([('m.', 'Monsieur'), ('mme', 'Madame'), ('mlle', 'Mademoiselle'), ('m. et mme', 'M. et Mme')],
                                string="Civilité", related='bailleur.civilite')

    nbre_tour = fields.Integer(string="niveau", related='bien_loue.nbre_tour')

    type_bien = fields.Many2one(related='bien_loue.type_id', string="Type Bien")

    categ_id = fields.Many2one(related='bien_loue.categ_id', string="Type Bien")

    adresse = fields.Many2one(related='bien_loue.adresse', string="adresse Bien")

    ville = fields.Many2one(related='bien_loue.ville', string="ville Bien")
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


    prixlocation_id = fields.Float(string="Prix de la location (hors charges en fcfa)",
                                   related='bien_loue.list_price', default=0.0)
    utilisation = fields.Selection([('utilisation1', 'D’HABITATION'),
                                    ('utilisation3', 'Utilisation professionnelle')], string="Utilisation")

    # champs----locataire
    locataires = fields.Many2one('res.partner', ondelete='cascade', string="Locataire")
    mobile = fields.Char(string="N° Tel Locataire", related='locataires.mobile')
    adresse_locataire = fields.Char(string="Adresse locataire",
                                    related='locataires.street')

    title = fields.Many2one(related='locataires.title')
    cin_ou_passeport = fields.Char(string="CIN ou passeport n°",
                                   related='locataires.num_piece_identite')

    # champs----Montant Déposé
    caution = fields.Float(string="montant déposé")
    date_depot = fields.Date(string="Date depot caution")

    depot_retourne = fields.Boolean('depot_retourne')
    maintenance = fields.Float(string="coût maintenance", default=0.0)
    date_returne = fields.Date(string="Date caution retouné")
    caution_returne = fields.Float(string="Caution A Returner", default=0.0, compute='_cautionreturne')

   
    @api.onchange('caution')
    def _cautionreturne(self):
            self.caution_returne = (self.caution * 1 / 3) - self.maintenance   
            
    

    # champs---information Contrat
    # validations de la date de debut et d'expiration
    date_debut = fields.Date(string="Date Début", required=True)
    date_expiration =  fields.Date(string="End Date", store=True,
        compute='_get_end_date')

    
    
    duration = fields.Float(default=365, help="Duration in days")

    @api.depends('date_debut', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.date_debut and r.duration):
                r.date_expiration = r.date_debut
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.date_expiration = r.date_debut + duration

   
  
  

    date_quittancement = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'),
         ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'),
         ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')],
        string="jour de quittancement", help="La date selon laquelle vos quittances seraient datées", required=True)
    # duré payement
    paiement = fields.Selection([('mensuel', 'Mensuel'), ('bimestriel', 'Bimestriel'), ('trimestriel', 'Trimestriel'),
                                 ('semestriel', 'Semestriel'), ('annuel', 'Annuel'), ('forfaitaire', 'Forfaitaire')],
                                string="Durée Paiements", required=True)

    #
    loyer_sans_charges = fields.Float(string="Prix de la location en fcfa", related='bien_loue.list_price', default=0.0,
                                      digits=dp.get_precision('Loyer hors charges'))
    frais_retard = fields.Float(string='Frais de retard (%)', default=0.0,
                                digits=dp.get_precision('Frais de retard (%)'))
    autre_paiement = fields.Float(string='Autre Paiements', digits=dp.get_precision('Autre Paiements'))
    description_autre_paiement = fields.Text(string="Autre Paiements : Description")
    enregistrement_paiement = fields.One2many('lb.paiement', 'paiement_id', string="Paiements")
    condition_particuliere = fields.Text(string="Conditions")
    reste_a_payer = fields.Float(string="Reste à payer", default=0.0, digits=dp.get_precision('Reste à Payer'))
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('lb.location'),
                                 index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")
    locataire_a_jour = fields.Selection([('oui', 'Oui'), ('non', 'Non')], string="Le locataire est-il à jour ?")



    @api.multi
    def print_report(self):
        return self.env.ref('location_biens.contrat_card').report_action(self)

    @api.multi
    def print_report_close(self):
        return self.env.ref('location_biens.contrat_card_close').report_action(self)

    # états/barre LOCATION
    state = fields.Selection([
        ('draft', 'New Contrat'),
        ('confirm', 'Contrat en cour'),
        ('ferme', 'Contrat Clos'),
    ], string='Status', readonly=True, default='confirm')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            self.depot_retourne = False

    def action_done(self):
        for rec in self:
            rec.state = 'ferme'
            self.depot_retourne = True

    

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
            bien.doc_count = Attachment.search_count([('res_model', '=', 'lb.location'), ('res_id', '=', bien.id)])

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'lb.location'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Cliquez sur Créer (et non importer) pour ajouter vos contrats de location</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }



    courtier = fields.Many2one('lb.courtier')

    mobile = fields.Char(string="Mobile coutier", related='courtier.mobile')

    active_commision = fields.Boolean('courtier_True')
    commision_courtier = fields.Float(string="Commision Courtier", default=0.0, compute='_commissioncourtier')

    @api.onchange('caution','active_commision')
    def _commissioncourtier(self):
        for r in self:
            if r.active_commision == True:
                r.commision_courtier = ((r.caution * 1 / 3) * 30) / 100


    commision_agence = fields.Float(string="Commision agence", default=0.0, compute='_commissionagence')

    @api.onchange('caution','active_commision')
    def _commissionagence(self):
        if self.active_commision == True:
            self.commision_agence = ((self.caution * 1 / 3) * 70) / 100
        else:
            self.commision_agence = (self.caution * 1 / 3)

    payement_avance = fields.Float(string="Mois avance", default=0.0, compute='_avance')

    @api.onchange('caution')
    def _avance(self):
            self.payement_avance = (self.caution * 1 / 3)

    #kanban
    color = fields.Integer()

    etat_count = fields.Integer(string='Etat Lieux', compute='get_etat_count')

    def get_etat_count(self):
        count = self.env['lb.etat_des_lieux'].search_count([('location', '=', self.id)])
        self.etat_count = count

    @api.multi
    def open_etat_contrat(self):
        return {
            'name': _('Etat_Lieux'),
            'domain': [('location', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.etat_des_lieux',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }



   


class Courtier(models.Model):
    _name = 'lb.courtier'
    _rec_name = 'nom_courtier'

    nom_courtier = fields.Char(string="Nom du Courtier")

    civilite = fields.Selection([('m.', 'M.'), ('mme', 'Mme'), ('mlle', 'Mlle'), ('m. et mme', 'M. et Mme')],
                                string="Civilité")
    email = fields.Char(string="E-mail", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    street = fields.Char(string="Adresse")
    ville = fields.Char(string="Ville")

    num_piece_identite = fields.Char(string='Numéro de la pièce d\'identité')

    contrat_count = fields.Integer(string='Contrats', compute='get_contrat_count')

    @api.multi
    def open_courtier_contrat(self):
        return {
            'name': _('Contrats'),
            'domain': [('courtier', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.location',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count(self):
        count = self.env['lb.location'].search_count([('courtier', '=', self.id)])
        self.contrat_count = count



    property_account_payable_id = fields.Many2one('account.account', company_dependent=True,
        string="compte courtier", oldname="property_account_payable",
        domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
        help="This account will be used instead of the default one as the payable account for the current partner",
        required=True)
        

class Paiement(models.Model):
    _name = 'lb.paiement'
    _rec_name = 'paiement_id'

    paiement_id = fields.Many2one('lb.location', string="Location")
    locataire_id = fields.Many2one(related='paiement_id.locataires', string="Locataire")
    loyer_sans_charges = fields.Float(related='paiement_id.loyer_sans_charges', string="Loyer charges comprises")
    fin_bail_id = fields.Date(related='paiement_id.date_expiration', string="Date Expiration")
    date_paiement = fields.Date(string="Date de Paiement")
    periode_paye_debut = fields.Date(string="Période Payée : Début", required=True)
    periode_paye_fin = fields.Date(string="Période Payée : Fin", required=True)
    montant_paye = fields.Float(string="Montant Payé", default=0.0, digits=dp.get_precision('Montant Payé'),
                                required=True)
    commentaire_paiement = fields.Text(string="Commentaire")
    objet_paiement = fields.Selection([('avance', 'Avance'), ('loyer', 'Loyer du mois'), ('pénalité', 'Pénalités'),
                                       ('autre paiements', 'Autres Paiements')], string="Objet du Paiement")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('lb.location'),
                                 index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')

    # Calcul de la devise
    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
            
            
            
            
            
            

