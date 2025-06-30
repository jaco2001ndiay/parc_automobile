from odoo import models, fields, api

class Client(models.Model):
    _name = 'parc.automobile.client'
    _description = "Client"
    
    name = fields.Char(string='Nom', required=True)
    adresse = fields.Text(string='Adresse')
    telephone = fields.Char(string='Téléphone')
    email = fields.Char(string='Email')
    image = fields.Binary(string="Photo")
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)