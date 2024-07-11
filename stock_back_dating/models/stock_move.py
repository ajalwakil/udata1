
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_backdate(self):
        self.ensure_one()
        backdate = self._context.get('backdate', False)
        print('uuuuuuuuuuuuuuuuuXXXXXXXXXXXXXXX',backdate)
        if self.picking_id and not self.picking_id.is_effective:
            date = self.picking_id.date_done
        elif backdate:
            date = backdate
        print('daaaaaaaaaaaaaaaaate',date)
        return date

    def _to_backdate_moves(self):
        to_backdate_moves = self.env["stock.move"]
        for move in self:
            if move.picking_id and not move.picking_id.is_effective:
                to_backdate_moves |= move
            elif  move._context.get('backdate', False):
                to_backdate_moves |= move
        return to_backdate_moves


    def _action_done(self, cancel_backorder=False):
        moves_todo = super()._action_done(cancel_backorder)
        moves_todo_backdate = self._to_backdate_moves()
        if moves_todo_backdate:
            moves_todo_backdate.mapped(
                lambda move: move.write(
                    {"date": move._get_backdate() or move.date}
                )
            )
            moves_todo_backdate.move_line_ids.mapped(
                lambda line: line.write(
                {"date": line.move_id._get_backdate() or line.move_id.date}))
            done_moves = moves_todo_backdate.filtered(lambda move: move.state == "done")
            to_update_valuation = done_moves.mapped("stock_valuation_layer_ids")
            if to_update_valuation:
                start_of_statement = "update stock_valuation_layer set create_date = d.create_date::timestamp from (values"
                val = [
                    "(%s,'%s')"
                    % (
                        svl.id,
                        svl.stock_move_id._get_backdate() or svl.create_date,
                    )
                    for svl in to_update_valuation
                ]
                end_of_statement = (
                    ") as d(id,create_date)  where stock_valuation_layer.id = d.id;"
                )
                moves_todo_backdate.env.cr.execute(
                    start_of_statement + ",".join(val) + end_of_statement
                )
        return moves_todo
