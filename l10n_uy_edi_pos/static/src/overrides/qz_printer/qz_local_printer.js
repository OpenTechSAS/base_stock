/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { QZTrayLocalPrinter } from "@pos_qz_printing_mobile/app/qz_printer/qz_local_printer";

patch(QZTrayLocalPrinter.prototype, {    

    async prepareDataToPrint(format, datavalue, options = {}) {
        const invoiceBase64 = this.env.services.pos.selectedOrder.invoice_base64;
        if (invoiceBase64) {            
            format = 'pdf';
            datavalue = invoiceBase64;            
        }
        return super.prepareDataToPrint(format, datavalue, options);
    }
});


