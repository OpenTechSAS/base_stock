# -*- coding: utf-8 -*-
from base64 import decodebytes, encodebytes
from io import BytesIO

from odoo import api, fields, models
from pdf2image import convert_from_bytes


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    def _prepare_invoice_vals(self):
        res = super(PosOrder, self)._prepare_invoice_vals()
        reversed_entry_id = self.refunded_order_id or False
        company_id = self.company_id.parent_id or self.company_id
        if self.uuid:
            res['uy_uuid'] = self.uuid
        if reversed_entry_id:
            res['reversed_entry_id'] = reversed_entry_id.account_move.id
        if self.partner_id.uy_doc_type=='2' and res.get('move_type', '') == 'out_refund':
            journal_id = self.env['account.journal'].search(
                [('type', '=', 'sale'), ('uy_document_code', '=', '112'),
                 ('company_id', '=', company_id.id),('uy_is_edi_document','=',True)], limit=1)
            if journal_id:
                res['uy_document_code'] = '112'
                res['journal_id'] = journal_id.id

        elif self.partner_id.uy_doc_type!='2' and res.get('move_type', '') == 'out_refund':
            journal_id = self.env['account.journal'].search(
                [('type', '=', 'sale'), ('uy_document_code', '=', '102'),
                 ('company_id', '=', company_id.id),('uy_is_edi_document','=',True)], limit=1)
            if journal_id:
                res['uy_document_code'] = '102'
                res['journal_id'] = journal_id.id
        elif self.partner_id.uy_doc_type=='2':
            journal_id = self.env['account.journal'].search(
                [('type', '=', 'sale'), ('uy_document_code', '=', '111'),
                 ('company_id', '=', company_id.id),('uy_is_edi_document','=',True)], limit=1)
            if journal_id:
                res['uy_document_code'] = '111'
                res['journal_id'] = journal_id.id
        else:
            journal_id = self.env['account.journal'].search(
                [('type', '=', 'sale'), ('uy_document_code', '=', '101'),
                 ('company_id', '=', company_id.id),('uy_is_edi_document','=',True)], limit=1)
            if journal_id:
                res['uy_document_code'] = '101'
                res['journal_id'] = journal_id.id
        return res
    
    def get_image_data_from_pdf(self, pdf_data):
        """
        Convert PDF data to image data.
        """
        images = convert_from_bytes(decodebytes(pdf_data))
        all_images = []
        # Process image
        for i in range(len(images)):
            grayscale = images[i].convert('L')
            file = BytesIO()
            grayscale.save(file, 'png')
            image_b64 = encodebytes(file.getvalue())
            width = grayscale.width % 2 != 0 and grayscale.width + 1 or grayscale.width
            all_images.append(
                {
                    'image': image_b64,
                    'height': grayscale.height,
                    'width': width,
                    'invoice_base64': pdf_data
                }
            )
        return all_images[0]

    def get_uy_pdf_invoice(self):
        self.ensure_one()
        vals = {}
        move_id = self.account_move.sudo()
        move_id.action_check_cfe_pdf_status()
        edi_document_id = move_id.uy_cfe_id
        if edi_document_id.attachment_id:
            vals['url'] = '/web/content/ir.attachment/%d/datas/%s' % (edi_document_id.attachment_id.id, edi_document_id.attachment_id.name)
            vals['invoice'] = self.get_image_data_from_pdf(edi_document_id.attachment_id.datas)
        if edi_document_id.error:
            vals['error'] = edi_document_id.error
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        """Cualquier orden que tenga lineas negativas y no sean de reembolso debemos ajusar los totales por error de odoo."""
        for vals in vals_list:
            if not any(line[2]['refunded_orderline_id'] for line in vals.get('lines', [])) and \
                vals.get('amount_total', 1) < 0:
                    vals['amount_total'] = 0.0
                    vals['amount_tax'] = 0.0
                    vals['amount_return'] = 0.0
        return super().create(vals_list)

    def _create_invoice(self, move_vals):
        res = super(PosOrder, self.with_context(uy_edi_pos_document=True))._create_invoice(move_vals=move_vals)
        res.invoice_line_ids._uy_invoice_indicator()
        if self.uuid:
            res.uy_uuid = self.uuid
        return res
