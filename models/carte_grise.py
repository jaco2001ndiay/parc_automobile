from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarteGrise(models.Model):
    _name = 'parc.automobile.carte.grise'
    _description = "Carte grise"
    
    name = fields.Char(
        string="Numéro", 
        required=True, 
        readonly=True,
        default="Nouveau"
    )
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Voiture",
        required=True
    )
    date_delivrance = fields.Date(
        string="Date de délivrance",
        required=True
    )
    lieu_delivrance = fields.Char(
        string="Lieu de délivrance",
        required=True
    )
    date_expiration = fields.Date(
        string="Date d'expiration",
        required=True
    )
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('parc.automobile.carte.grise') or 'Nouveau'
        return super().create(vals_list)
    
    @api.constrains('date_delivrance', 'date_expiration')
    def _check_dates(self):
        for record in self:
            if record.date_delivrance > record.date_expiration:
                raise ValidationError("La date de délivrance ne peut pas être postérieure à la date d'expiration")