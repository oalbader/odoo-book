{
        'name': 'To-Do Application',
        'description': 'Manage personal to-do tasks.',
        'author': 'Omar Albader',
        'depends': ['base'],
        'application': True,
        'data': [
            'security/ir.model.access.csv',
            'security/todo_access_rules.xml',
            'views/todo_menu.xml',
            'views/todo_view.xml',
            'views/res_partner_view.xml',
            'views/index_template.xml',
        ],
        'demo': [
            'data/todo.task.csv',
            'data/todo_task.xml',
        ],
}
