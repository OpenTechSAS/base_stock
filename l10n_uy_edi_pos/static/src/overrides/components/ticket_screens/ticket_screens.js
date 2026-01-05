import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    setPartnerToRefundOrder(partner, destinationOrder) {
        if (!destinationOrder || !partner) {
            return;
        }

        const current = destinationOrder.get_partner && destinationOrder.get_partner();
        const anonId =
            (this.pos && this.pos.session && this.pos.session._uy_anonymous_id) ||
            (this.env?.pos?.session?._uy_anonymous_id);

        // La refund order no tiene partner
        if (!current) {
            destinationOrder.set_partner(partner);
            return;
        }

        //La refund order tiene partner pero no coincide con la original
        if (anonId && current.id === anonId && partner.id !== anonId) {
            destinationOrder.set_partner(partner);
        }
    },
});
