from odoo import api, fields, models

class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task', 'mail.thread']
    effort_estimate = fields.Integer()
    name = fields.Char(help="What needs to be done?")
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')
    stage_fold = fields.Boolean(
            'Stage Folded?',
            compute='_compute_stage_fold',
            search='_search_stage_fold',
            inverse='_write_stage_fold')
    state = fields.Selection(
            related='stage_id.state',
            string='Stage State')
    
    _sql_constraints = [
            ('todo_task_name_uniq',
             'UNIQUE (name, active)',
             'Task title must be unique!')
            ]

    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for todo in self:
            todo.stage_fold = todo.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        for todo in self:
            todo.stage_id.fold = todo.stage_fold

    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name) < 5:
                raise ValidationError('Must have 5 characters!')

    @api.onchange('user_id')
    def onchange_user_id(self):
        if not self.user_id:
            self.team_ids = None
            self.message_post('Hello', subtype='mail.mt_comment')
            return {
                'warning': {
                    'title': 'No Responsible',
                    'message': 'Team was also reset.'
                }
            }
