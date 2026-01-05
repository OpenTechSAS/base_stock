# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from pyCFE import Servidor


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    days_to_clean = fields.Selection([
            ('30', 'Mas de 30 dias'), 
            ('60', 'Mas de 60 dias'), 
            ('90', 'Mas de 90 dias'),
        ],
        config_parameter='l10n_uy_edi_cfe.days_to_clean',
        string='Dias para limpiar CFEs',
        default='30',
        help='Dias de antiguedad para limpiar los archivos'
    )

    def action_cfe_config_wizard(self):
        self.ensure_one()
        context = dict(self.env.context)
        context['active_id'] = self.id
        return {
            'name': _('CFE Wizard'),
            'res_model': 'uy.cfe.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('l10n_uy_edi_cfe.view_form_uy_cfe_wizard').id,
            'context': context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('l10n_uy_edi_cfe.days_to_clean', self.days_to_clean)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            days_to_clean=self.env['ir.config_parameter'].get_param('l10n_uy_edi_cfe.days_to_clean'),
        )
        return res
