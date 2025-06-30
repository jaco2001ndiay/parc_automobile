from odoo import models, fields, api

class Modele(models.Model):
    _name = 'parc.automobile.modele'
    _description = "Modèle" 
    
    name = fields.Char(string='Nom', required=True)
    marque_id = fields.Many2one(
        'parc.automobile.marque', 
        string="Marque",
        required=True
    )
    type_carrosserie = fields.Selection([
        ('berline', 'Berline'),
        ('suv', 'SUV'),
        ('4x4', '4x4'),
        ('break', 'Break'),
        ('cabriolet', 'Cabriolet'),
        ('monospace', 'Monospace')
    ], string='Type de carrosserie', default='berline')
    consommation = fields.Float(string='Consommation (L/100km)')
    puissance = fields.Integer(string='Puissance (ch)')
    image = fields.Binary(string="Image")
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)