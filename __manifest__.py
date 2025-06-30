{
    'name': 'parc_automobile',
    'version': '1.4',
    'summary': "Module de gestion de parc automobile pour Odoo 18",
    'sequence': -200,
    'description': "Gestion complète du parc automobile : véhicules, entretiens, assurances, affectations...",
    'category': 'Fleet Management',
    'website': 'https://github.com/jaco2001ndiay/',
    'depends': ['base', 'mail', 'web', 'hr'],
    'data': [
        # Sécurité
        'security/parc_automobile_security.xml',
        'security/ir.model.access.csv',
        
        
        # Données
        'data/ir_sequence.xml',
        'data/cron_jobs.xml',
        'data/email_templates.xml',
        
        # Rapports
        'report/reports.xml',
        'report/templates/voiture_report.xml',
        
        # Vues
        'views/menu.xml',
        'views/client.xml',
        'views/marque.xml',
        'views/modele.xml',
        'views/voiture.xml',
        'views/assurance.xml',
        'views/carte_grise.xml',
        'views/contrat_location.xml',
        'views/employe.xml',
        'views/entretien.xml',
        'views/affectation.xml',
        'views/carburant.xml',
        'views/res_users.xml',
        'views/document.xml',
        'views/dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # CSS
            'parc_automobile/static/src/css/dashboard.css',
            
            # JS
            'parc_automobile/static/src/js/dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'author': "Francois Thiombane",
    'auto_install': False,
}