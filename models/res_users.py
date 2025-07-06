from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    job_title = fields.Char(string="Titre du poste")
    
    @api.model_create_multi
    def create(self, vals_list):
        # Pas de logique de séquence nécessaire
        return super().create(vals_list)
    
    # Remove the problematic constraint from here
    # We'll move it to the hr.employee model instead
    
    def get_associated_employee(self):
        """Méthode utilitaire pour récupérer l'employé associé"""
        self.ensure_one()
        return self.employee_ids[0] if self.employee_ids else False