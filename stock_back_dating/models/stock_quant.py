
from odoo import models, fields, api, _
from odoo.tools.misc import groupby
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    modify_date = fields.Boolean(
        copy=False,
        help="Enabling it will backdate created stock move, and svl to Accounting Date", string="Backdating stock"
    )

    def _apply_inventory(self):
        for accounting_date, inventory_ids in groupby(self, key=lambda q: q.modify_date and q.accounting_date):
            inventories = self.env['stock.quant'].concat(*inventory_ids)
            if accounting_date:
                super(StockQuant, inventories.with_context(backdate=accounting_date))._apply_inventory()
                inventories.modify_date = False
            else:
                super(StockQuant, inventories)._apply_inventory()

    @api.model
    def _get_inventory_fields_write(self):
        res = super()._get_inventory_fields_write()
        res += ['modify_date']
        return res

    @api.model
    def _get_inventory_fields_create(self):
        res = super()._get_inventory_fields_create()
        res += ['modify_date']
        return res

    @api.model_create_multi
    def create(self, vals_list):
        is_inventory_mode = self._is_inventory_mode()
        allowed_fields = self._get_inventory_fields_create()
        for vals in vals_list:
            if is_inventory_mode and any(f in vals for f in ['inventory_quantity', 'inventory_quantity_auto_apply']):
                if any(field for field in vals.keys() if field not in allowed_fields):
                    raise UserError(_("Quant's creation is restricted, you can't do this operation."))
                product = self.env['product.product'].browse(vals['product_id'])
                location = self.env['stock.location'].browse(vals['location_id'])
                lot_id = self.env['stock.lot'].browse(vals.get('lot_id'))
                package_id = self.env['stock.quant.package'].browse(vals.get('package_id'))
                owner_id = self.env['res.partner'].browse(vals.get('owner_id'))
                quant = self.env['stock.quant']
                if not self.env.context.get('import_file'):
                    quant = self._gather(product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)
                if lot_id:
                    quant = quant.filtered(lambda q: q.lot_id)
                if quant:
                    quant = quant[0].sudo()
                    quant.modify_date = vals.get('modify_date')
                    quant.accounting_date = vals.get('accounting_date')
        res = super().create(vals_list)
        return res
