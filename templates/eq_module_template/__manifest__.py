

{
    'name': 'Equitania Module Template',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'description': """
        Module Template for eq v10 modules
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup'],
    'category' : 'General Improvements',
    'summary': 'Module Template',

    'data': [
        #"security/ir.model.access.csv"
        "views/templates.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
