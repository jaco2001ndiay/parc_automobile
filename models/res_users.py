from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    job_title = fields.Char(string="Titre du poste")
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)
    
    @api.constrains('employee_ids')
    def _check_employee_user(self):
        """Empêcher plusieurs utilisateurs pour le même employé"""
        for user in self:
            if user.employee_id:
                existing = self.search([
                    ('employee_id', '=', user.employee_id.id),
                    ('id', '!=', user.id)
                ], limit=1)
                if existing:
                    raise ValidationError("Cet employé est déjà associé à un autre utilisateur")
    
    def get_associated_employee(self):
        """Simplified method using standard fields"""
        self.ensure_one()
        return self.employee_ids[0] if self.employee_ids else False