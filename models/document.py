from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

class Document(models.Model):
    _name = 'parc.automobile.document'
    _description = "Documents administratifs"
    
    name = fields.Selection([
        ('ct', 'Contrôle Technique'),
        ('vignette', 'Vignette'),
        ('assurance', 'Attestation Assurance'),
        ('carte_grise', 'Carte Grise')
    ], string="Type de document", required=True)
    voiture_id = fields.Many2one(
        'parc.automobile.voiture', 
        string="Véhicule", 
        required=True
    )
    date_emission = fields.Date(
        string="Date d'émission",
        required=True
    )
    date_expiration = fields.Date(
        string="Date d'expiration",
        required=True
    )
    fichier = fields.Binary(string="Fichier")
    note = fields.Text(string="Notes")

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    @api.constrains('date_emission', 'date_expiration')
    def _check_dates(self):
        for record in self:
            if record.date_emission > record.date_expiration:
                raise ValidationError("La date d'émission ne peut pas être postérieure à la date d'expiration")
    
    def _check_expired_documents(self):
        today = fields.Date.today()
        expired_docs = self.search([('date_expiration', '<', today)])
        # Envoyer une notification par email
        # ...
    
    def _send_expiration_notifications(self):
        """Envoyer des notifications pour les documents expirant dans 30 jours"""
        today = fields.Date.today()
        expiration_date = date_utils.add(today, days=30)
        expiring_docs = self.search([
            ('date_expiration', '<=', expiration_date),
            ('date_expiration', '>=', today)
        ])
        # Envoyer les notifications
        # ...