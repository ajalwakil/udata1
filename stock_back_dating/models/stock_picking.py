
import pytz

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_done = fields.Datetime(default=lambda self: fields.Datetime.now())

    is_effective = fields.Boolean("Today is the effective date", default=True)
    active = fields.Boolean('Active', default=True)


    def button_validate(self):

        if not self.is_effective:
            effective_date = self.date_done.date() if self.date_done else False
            if effective_date and not self._context.get("force_period_date", False):
                destination_tz = pytz.timezone(self.env.user.tz or "UTC")
                effective_date = pytz.utc.localize(self.date_done).astimezone(
                    destination_tz
                )
                self = self.with_context(force_period_date=effective_date.date())
        return super().button_validate()

    def _action_done(self):
        date_done = self.date_done

        res = super()._action_done()
        if not self.is_effective and date_done:
            self.date_done = date_done
            self.move_line_ids.date = self.date_done
        return res
