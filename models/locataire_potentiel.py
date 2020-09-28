# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp



class Locataire_potenciel(models.Model):
    _inherit = 'res.partner'

    quartier_souhaitee = fields.Many2one('lb.quartier', string="Quartier souhaité")
    budget = fields.Float(string="Budget", default=0.0, digits=dp.get_precision('Budget'))
    #type_id = fields.Many2one('lb.type', string="Type Biens souhaitee")


    active_potenctiel = fields.Selection(
        [('client', 'Est Un Client'), ('prospect', 'Est Un Prospect')],
        string="statut", required=True, default='client')



    reclamation = fields.One2many('lb.reclamation', 'reclamation_id',
                                             string="Fiche de réclamation", required=True)

    origine_prospect = fields.Selection(
        [('pub_journal', 'Pub journal'), ('site_web', 'Site web CPI'), ('linkedIn', 'LinkedIn'),
         ('facebook', 'Facebook'), ('agent_cpi', 'Agent CPI'), ('recommande', 'Recommandé')],
        string="ORIGINE DU PROSPECT")

    user_id = fields.Many2one('res.users', string='Agent-Guide', track_visibility='onchange',
                              default=lambda self: self.env.user)

    # user_id = fields.Many2one('res.users', string='Agent-cpi')

    nbre_tour = fields.Integer(string="niveau souhaité", default=0)
    ameublement = fields.Char(string="ameublement souhaité")
    chambres = fields.Float(string="Nombre Chambres souhaité", default=0)
    salons = fields.Float(string="Nbre Salons souhaité", default=0)
    cuisines = fields.Float(string="Nbre Cuisines souhaité", default=0)
    toilette = fields.Float(string="Nbre Toilettes souhaité", default=0)
    cour = fields.Float(string="espace familiale souhaité", default=0)




    contrat_count = fields.Integer(string='Contrats', compute='get_contrat_count')

    @api.multi
    def open_locataire_contrat(self):
        return {
            'name': _('Contrats location'),
            'domain': [('locataires', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.location',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count(self):
        count = self.env['lb.location'].search_count([('locataires', '=', self.id)])
        self.contrat_count = count
        
    #vente    
        
    contrat_count_vente = fields.Integer(string='Contrats vente', compute='get_contrat_count_vente')

    @api.multi
    def open_locataire_contrat_vente(self):
        return {
            'name': _('Contrats vente'),
            'domain': [('locataires', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.contrat_vente',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_contrat_count_vente(self):
        count = self.env['lb.contrat_vente'].search_count([('locataires', '=', self.id)])
        self.contrat_count_vente = count

        

    besoin = fields.Selection(
        [('location', 'Location Bien'), ('ach', 'Achat Biens')],
        string="Besoin Du Prospect")

    type_besoin = fields.Char(string="type de besoin")


    client_type = fields.Selection(
        [('client_ache', 'Client Acheteur'), ('client_loc', 'Client Locataire')],
        string="statut client")


class reclamation(models.Model):
    _name = 'lb.reclamation'

    reclamation_id = fields.Many2one('res.partner', ondelete='cascade', string="Réclamation")
    type_reclamation = fields.Selection(
        [('reparataion', 'demande de réparation'), ('payement', 'payement'),
         ('voisin', 'Vie locative'),('amenagement', 'autorisatio de faire des travaux'),('resiliation', 'Résiliation du bail et Sortie')], string="Type Réclamation")
    date_reclamation = fields.Date('Date Réclamation')

    resume_reclamation = fields.Char(string="Résumé")
    notes = fields.Html('Description', sanitize_style=True)
    fichier = fields.Binary(string="fichier", attachment=True)

    @api.multi
    def action_close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def action_done(self):
        """ Wrapper without feedback because web button add context as
        parameter, therefore setting context to feedback """
        return self.action_feedback()

    def action_feedback(self, feedback=False):
        message = self.env['mail.message']
        if feedback:
            self.write(dict(feedback=feedback))

    
   

class Locataire_potenciel_suite(models.Model):
    _inherit = 'res.partner'


    
    facture_count = fields.Integer(string='Factures', compute='get_facture_count')

    @api.multi
    def open_facture(self):
        return {
            'name': _('Factures'),
            'domain': [('locataire_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'lb.paiement_location',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_facture_count(self):
        count = self.env['lb.paiement_location'].search_count([('locataire_id', '=', self.id)])
        self.facture_count = count   



        

class Locataire_agent(models.Model):
    _inherit = 'res.partner'

        
    statut_agent = fields.Selection(
        [('bailleur', 'Est Un Bailleur'), ('courtier', 'Est Un Courtier')],
        string="statut", required=True, default='bailleur')
        

 
