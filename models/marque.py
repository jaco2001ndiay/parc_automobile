from odoo import models, fields, api

class Marque(models.Model):
    _name = 'parc.automobile.marque'
    _description = "Marque"
    
    name = fields.Char(string='Nom', required=True)
    pays_id = fields.Many2one(
        'res.country', 
        string="Pays d'origine",
        required=True
    )
    date_creation = fields.Date(string="Année de fondation")
    logo = fields.Binary(string="Logo")
    modele_ids = fields.One2many(
        'parc.automobile.modele', 
        'marque_id', 
        string='Modèles'
    )
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)