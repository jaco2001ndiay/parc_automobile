from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Affectation(models.Model):
    _name = 'parc.automobile.affectation'
    _description = "Affectation véhicule à un conducteur"
    
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Véhicule", 
        required=True
    )
    employe_id = fields.Many2one(
        'hr.employee', 
        string="Conducteur", 
        required=True
    )
    date_debut = fields.Date(
        string="Date de début", 
        default=fields.Date.today,
        required=True
    )
    date_fin = fields.Date(string="Date de fin")
    type_affectation = fields.Selection([
        ('permanent', 'Permanent'),
        ('temporaire', 'Temporaire')
    ], string="Type d'affectation", default='permanent')
    
    _sql_constraints = [
        ('date_check', 
         "CHECK (date_debut <= date_fin)", 
         "La date de début doit être antérieure à la date de fin.")
    ]
    @api.model_create_multi
    def create(self, vals_list):
        # Pas de logique de séquence nécessaire
        return super().create(vals_list)
    @api.constrains('voiture_id', 'date_debut', 'date_fin')
    def _check_affectation_overlap(self):
        for record in self:
            domain = [
                ('voiture_id', '=', record.voiture_id.id),
                ('id', '!=', record.id),
                '|',
                '&', ('date_debut', '<=', record.date_fin),
                ('date_fin', '>=', record.date_debut),
                '&', ('date_debut', '<=', record.date_debut),
                ('date_fin', '=', False)
            ]
            if record.date_fin:
                overlapping = self.search(domain, limit=1)
                if overlapping:
                    raise ValidationError("Ce véhicule est déjà affecté pendant cette période")