from odoo import models, fields, api

class ParcAutomobileDashboard(models.Model):
    _name = 'parc.automobile.dashboard'
    _description = "Tableau de Bord Parc Automobile"
    
    @api.model
    def get_dashboard_data(self):
        # Statistiques de base
        voiture_count = self.env['parc.automobile.voiture'].search_count([])
        entretien_count = self.env['parc.automobile.entretien'].search_count([])
        affectation_count = self.env['parc.automobile.affectation'].search_count([])
        
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)        
        # Documents expirés
        expired_docs = self.env['parc.automobile.document'].search_count([
            ('date_expiration', '<', fields.Date.today())
        ])
        
        # Véhicules nécessitant un entretien
        maintenance_needed = self.env['parc.automobile.voiture'].search_count([
            ('etat', '=', 'en_entretien')
        ])
        
        # Consommation de carburant (exemple)
        fuel_data = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'values': [8.2, 7.9, 8.5, 9.1, 8.7, 8.3]
        }
        
        # État des véhicules
        Vehicle = self.env['parc.automobile.voiture']
        states = {
            'disponible': Vehicle.search_count([('etat', '=', 'disponible')]),
            'en_utilisation': Vehicle.search_count([('etat', '=', 'en_utilisation')]),
            'en_entretien': Vehicle.search_count([('etat', '=', 'en_entretien')]),
            'hors_service': Vehicle.search_count([('etat', '=', 'hors_service')]),
        }
        
        return {
            'voiture_count': voiture_count,
            'entretien_count': entretien_count,
            'affectation_count': affectation_count,
            'expired_docs': expired_docs,
            'maintenance_needed': maintenance_needed,
            'fuel_consumption': fuel_data,
            'vehicle_states': {
                'labels': list(states.keys()),
                'values': list(states.values())
            },
            'actions': {
                'voitures': self.env.ref('parc_automobile.action_voiture').id,
                'entretiens': self.env.ref('parc_automobile.action_entretien').id,
                'documents': self.env.ref('parc_automobile.action_document').id,
            }
        }