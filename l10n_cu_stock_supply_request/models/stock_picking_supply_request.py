# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class SupplyRequest(models.Model):

    _name = 'stock_picking.supply_request'
    _description = "Supply request"
    _order = 'name'
    _inherits = {'stock.picking': 'picking_id'}

    picking_id = fields.Many2one('stock.picking', 'Operation', required=True, readonly=True, index=True,)
    # partner_id = fields.Many2one('res.partner', 'Contact', check_company=True,
    #                                 states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
    #                                 default=lambda self: self.env.user.partner_id)

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            if 'partner_id' in values:
                values['partner_id'] = self.env.user.partner_id.id
            else:
                values['partner_id'] = self.env.user.partner_id.id
        return super(SupplyRequest, self).create(values_list)



