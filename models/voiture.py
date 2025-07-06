from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Voiture(models.Model):
    _name = 'parc.automobile.voiture'
    _description = 'Voiture'
    
    name = fields.Char(
        string="Immatriculation", 
        required=True
    )
    marque_id = fields.Many2one(
        'parc.automobile.marque', 
        string="Marque"
    )
    modele_id = fields.Many2one(
        'parc.automobile.modele', 
        string="Modèle"
    )
    annee_fabrication = fields.Date(string="Année de fabrication")
    kilometrage = fields.Integer(
        string="Kilométrage", 
        default=0
    )
    couleur = fields.Char(string="Couleur")
    image = fields.Binary(string="Photo")
    etat = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_utilisation', 'En utilisation'),
        ('en_entretien', 'En entretien'),
        ('hors_service', 'Hors service')
    ], string="État", default='disponible')
    assurance_id = fields.Many2one(
        'parc.automobile.assurance', 
        string="Assurance"
    )
    carte_grise_id = fields.Many2one(
        'parc.automobile.carte.grise', 
        string="Carte grise"
    )
    affectation_ids = fields.One2many(
        'parc.automobile.affectation', 
        'voiture_id', 
        string="Affectations"
    )
    entretien_ids = fields.One2many(
        'parc.automobile.entretien', 
        'voiture_id', 
        string="Entretiens"
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
    @api.constrains('name')
    def _check_immatriculation(self):
        for record in self:
            if len(record.name) < 5:
                raise ValidationError("L'immatriculation doit avoir au moins 5 caractères")