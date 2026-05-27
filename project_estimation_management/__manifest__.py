{
    'name': 'Project Estimation Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage Project Cost Estimations',
    'description': 'Custom module for project estimation and costing',
    'author': 'QWY_LK',
    'category': 'Project',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'sale', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/project_estimation_views.xml',
        'views/project_industry_views.xml',
        'views/project_module_master_views.xml',

        'views/estimation_menu.xml',
        'report/estimation_report.xml',
        'report/estimation_template.xml',
    ],
    'installable': True,
    'application': True,
}
