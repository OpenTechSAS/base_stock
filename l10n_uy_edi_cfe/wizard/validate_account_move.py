from odoo import _, api, models


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    def validate_move(self):
        # Marcamos en el contexto que estamos en un posteo masivo sensible a Biller
        self = self.with_context(biller_batch_post=True)
        return super().validate_move()
