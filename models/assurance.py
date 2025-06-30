from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Assurance(models.Model):
    _name = 'parc.automobile.assurance'
    _description = "Assurance automobile"
    
    name = fields.Char(string="Compagnie d'assurance", required=True)
    numero_police = fields.Char(string="Numéro de police", required=True)
    type_assurance = fields.Selection([
        ('tiers', 'Au tiers'),
        ('intermediaire', 'Intermédiaire'),
        ('tout_risque', 'Tout Risque')
    ], string="Type d'assurance", default='tiers')
    date_debut = fields.Date(string="Date de début", required=True)
    date_fin = fields.Date(string="Date de fin", required=True)
    montant_annuel = fields.Float(string='Montant annuel')
    voiture_ids = fields.One2many(
        'parc.automobile.voiture', 
        'assurance_id', 
        string='Voitures assurées'
    )
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        for record in self:
            if record.date_fin < record.date_debut:
                raise ValidationError("La date de fin doit être postérieure à la date de début")