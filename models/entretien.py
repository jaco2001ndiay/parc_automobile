from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Entretien(models.Model):
    _name = 'parc.automobile.entretien'
    _description = "Entretien"
    
    name = fields.Char(
        string="Référence", 
        readonly=True,
        default="Nouveau"
    )
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Voiture",
        required=True
    )
    type_entretien = fields.Selection([
        ('vidange', 'Vidange'),
        ('changement_pieces', 'Changement des pièces'),
        ('revision', 'Révision'),
        ('reparation', 'Réparation')
    ], string="Type d'entretien", default='vidange')
    date_entretien = fields.Date(
        string="Date d'entretien", 
        default=fields.Date.today,
        required=True
    )
    cout = fields.Float(
        string='Coût',
        required=True
    )
    date_prochain_entretien = fields.Date(string="Prochain entretien")
    description = fields.Text(string="Description")
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('parc.automobile.entretien') or 'Nouveau'
        return super().create(vals_list)    
    @api.constrains('cout')
    def _check_cout(self):
        for record in self:
            if record.cout < 0:
                raise ValidationError("Le coût ne peut pas être négatif")