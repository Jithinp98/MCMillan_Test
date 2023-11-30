from odoo import api, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # if domain is None:
        #     domain = []

        team = self.env['crm.team'].search([('user_id', '=', self.env.user.id)]).mapped('member_ids')
        print('TEAM', team.id)
        print('USER', self.env.user.id)

        if self.env.user.has_group('sales_team.group_sale_manager'):
            domain += ['|', ('user_id', 'in', team.id), ('user_id', '=', self.env.user.id)]
        else:
            domain += []

        print('Domain', domain)

        return super(CrmLead, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
