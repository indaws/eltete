# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ampliaciones Odoo ELTETE",
    "summary": "Ampliaciones para ELTETE",
    'version': '12.0.1.0.0',
    "category": "Customer Relationship Management",
    "website": "www.puntsistemes.es",
    "author": "PUNT SISTEMES",

    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "sale",
        "product",
        "sale_stock",
        "account",
        "stock_picking_invoice_link"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/product_template.xml",
        "views/sale_offer.xml",
        "views/sale_cotizacion.xml",
        "views/stock_production_lot.xml",
        "views/sale_order.xml",
        "views/pricelist_oferta.xml",
        "reports/qweb/report_sale_cotizacion.xml",
        "reports/qweb/report_sale_orden_fabricacion.xml",
        "reports/qweb/report_etiquetas_pedido.xml",
        "reports/eltete_report.xml",
        
    ],

}
