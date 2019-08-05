from odoo import models, fields, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    _description = 'To-do Mass Assignment'
    task_ids = fields.Many2many(
            'todo.task',
            string='Tasks')
    new_deadline = fields.Date('Deadline to set')
    new_user_id = fields.Many2one(
            'res.users',
            string='Responsible to set')

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        defaults['task_ids'] = self.env.context['active_ids']
        return defaults

    @api.multi
    def do_mass_update(self):
        for todo in self:
            if not (todo.new_deadline or todo.new_user_id):
                raise exceptions.ValidationError('No data to update!')
            # Loggin debug messages
            _logger.debug(
                    'Mass update on Todo Tasks %s',
                    todo.task_ids.ids)
            vals = {}
            if todo.new_deadline:
                vals['date_deadline'] = todo.new_deadline
            if todo.new_user_id:
                vals['user_id'] = todo.new_user_id
            # Mass write values on all selected tasks
            if vals:
                todo.task_ids.write(vals)
        return True

    @api.multi
    def do_count_tasks(self):
        Task = self.env['todo.task']
        count = Task.search_count([('is_done', '=', False)])
        raise exceptions.Warning(
                'There are %d active tasks.' %count)
