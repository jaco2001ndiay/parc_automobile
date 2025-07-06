from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    @api.onchange('user_id')
    def _onchange_user_id(self):
        """Synchroniser le champ employee_id sur l'utilisateur"""
        for employee in self:
            if employee.user_id:
                employee.user_id.employee_id = employee
    affectation_ids = fields.One2many(
        'parc.automobile.affectation', 
        'employe_id', 
        string="Affectations"
    )
    voiture_actuelle_id = fields.Many2one(
        'parc.automobile.voiture',
        string="Voiture actuelle",
        compute='_compute_voiture_actuelle',
        store=True
    )
    date_embauche = fields.Date(string="Date d'embauche")
    date_fin_contrat = fields.Date(string="Date de fin de contrat")
    salaire = fields.Float(string="Salaire")
    permis_conduire = fields.Char(string="Numéro permis")
    @api.model_create_multi
    def create(self, vals_list):
        # Pas de logique de séquence nécessaire
        return super().create(vals_list)
    @api.depends('affectation_ids', 'affectation_ids.date_fin')
    def _compute_voiture_actuelle(self):
        today = fields.Date.today()
        for emp in self:
            # Optimisation : limiter la recherche
            affectation_active = self.env['parc.automobile.affectation'].search([
                ('employe_id', '=', emp.id),
                ('date_debut', '<=', today),
                '|',
                ('date_fin', '=', False),
                ('date_fin', '>=', today)
            ], order='date_debut desc', limit=1)
            
            emp.voiture_actuelle_id = affectation_active.voiture_id if affectation_active else False
    @api.constrains('date_embauche', 'date_fin_contrat')
    def _check_dates(self):
        for record in self:
            if record.date_fin_contrat and record.date_fin_contrat < record.date_embauche:
                raise ValidationError("La date de fin de contrat ne peut pas être antérieure à la date d'embauche")

    @api.constrains('salaire')
    def _check_salaire(self):
        for record in self:
            if record.salaire < 0:
                raise ValidationError("Le salaire ne peut pas être négatif")

    @api.constrains('user_id')
    def _check_employee_user(self):
        """Ensure only one user per employee"""
        for employee in self:
            if employee.user_id:
                existing = self.search([
                    ('user_id', '=', employee.user_id.id),
                    ('id', '!=', employee.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        "Cet employé est déjà associé à un autre utilisateur"
                    )