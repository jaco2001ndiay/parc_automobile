from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Carburant(models.Model):
    _name = 'parc.automobile.carburant'
    _description = "Suivi des consommations de carburant"
    
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Véhicule", 
        required=True
    )
    date = fields.Date(
        string="Date", 
        default=fields.Date.today,
        required=True
    )
    quantite_litre = fields.Float(
        string="Quantité (L)", 
        required=True
    )
    prix_litre = fields.Float(
        string="Prix par litre (€)", 
        required=True
    )
    kilometrage = fields.Integer(
        string="Kilométrage", 
        required=True
    )
    cout_total = fields.Float(
        string="Coût total (€)", 
        compute='_compute_cout', 
        store=True
    )
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
    @api.depends('quantite_litre', 'prix_litre')
    def _compute_cout(self):
        for record in self:
            record.cout_total = record.quantite_litre * record.prix_litre

    @api.constrains('quantite_litre', 'prix_litre')
    def _check_values(self):
        for record in self:
            if record.quantite_litre <= 0:
                raise ValidationError("La quantité doit être positive")
            if record.prix_litre <= 0:
                raise ValidationError("Le prix par litre doit être positif")