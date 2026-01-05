/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";

patch(TicketScreen.prototype, {
    setup() {
        super.setup();
        this._printUyReceipt()
    },

    
    async _printUyReceipt() {
        const order = this.getSelectedOrder();
        
        if (!(Number.isInteger(order.id))) return;

        if (order.id){
            const data = await this.pos.data.call("pos.order", "get_uy_pdf_invoice", [order.id]);
            if (data.error){
                alert(data.error);
            }
            if (data.invoice) {
                order.uy_invoice = "data:image/png;base64,"+ data.invoice.image;
                order.uy_height = data.invoice.height;
                order.uy_width = data.invoice.width;
                order.invoice_base64 = data.invoice.invoice_base64;
            }
        }
     },

});