from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ContratLocation(models.Model):
    _name = 'parc.automobile.contrat.location'
    _description = "Contrat de location" 
    
    name = fields.Char(
        string="Référence", 
        readonly=True,
        default="Nouveau"
    )
    date_debut = fields.Date(
        string="Date de début",
        required=True
    )
    date_fin = fields.Date(
        string="Date de fin",
        required=True
    )
    montant_total = fields.Float(
        string="Montant total",
        required=True
    )
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Voiture",
        required=True
    )
    client_id = fields.Many2one(
        'parc.automobile.client', 
        string="Client",
        required=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('parc.automobile.contrat.location') or 'Nouveau'
        return super().create(vals)
    
    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        for record in self:
            if record.date_fin < record.date_debut:
                raise ValidationError("La date de fin doit être postérieure à la date de début")