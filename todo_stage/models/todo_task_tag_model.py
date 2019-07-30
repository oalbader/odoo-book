from odoo import fields, models

class Tag(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'
    _parent_store = True

    name = fields.Char('Name', translate=True)
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)

