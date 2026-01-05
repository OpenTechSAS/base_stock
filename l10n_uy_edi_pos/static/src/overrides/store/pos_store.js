import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";


patch(PosStore.prototype, {

    // override
    /*async printReceipt({
                basic = false,
                order = this.get_order(),
                printBillActionTriggered = false,
            } = {}) {
        if (order.is_uruguayan_company()) {
            if (order.uy_order_server_id && !order.uy_invoice){
                const data = await this.pos.data.call("pos.order", "get_uy_pdf_invoice", [order.uy_order_server_id]);
                if (data.error){
                    alert(data.error);
                }
                if (data.invoice) {
                    order.uy_invoice = "data:image/png;base64,"+ data.invoice.image;
                    order.uy_height = data.invoice.height;
                    order.uy_width = data.invoice.width;
                }
            }
        }
        return super.printReceipt(...arguments);
    },*/
    isUruguayanCompany() {
        return this.company.country_id?.code == "UY";
    },
    createNewOrder() {
        const order = super.createNewOrder(...arguments);

        if (this.isUruguayanCompany() && !order.partner_id) {
            order.update({ partner_id: this.session._uy_anonymous_id });
        }

        return order;
    },

    async printReceipt({ basic = false, order = this.get_order() } = {}) {
        if ((Number.isInteger(order.id)))
            if (order.id){
                const data = await this.data.call("pos.order", "get_uy_pdf_invoice", [order.id]);
                if (data.error){
                    alert(data.error);
                }
                if (data.invoice) {
                    this.setOrderFromDataResult(order, data);
                }
            }
        return super.printReceipt(...arguments);
    },

    setOrderFromDataResult(order=this.get_order(), data) {
        order.uy_invoice = "data:image/png;base64,"+ data.invoice.image;
        order.uy_height = data.invoice.height;
        order.uy_width = data.invoice.width;
        order.invoice_base64 = data.invoice.invoice_base64;        
    },

    getBase64Invoice() {
        const order = this.get_order();
        return order.invoice_base64;
    },

});
