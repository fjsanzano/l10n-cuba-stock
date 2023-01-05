# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from tempfile import TemporaryFile
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from  datetime import datetime
import base64
from odoo.tools import pycompat
import logging

_logger = logging.getLogger(__name__)

try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None


class StockImportProductFromExcel(models.TransientModel):
    _name = "l10n_cu_stock_import.product_from_excel"
    _description = ""

    location_id = fields.Many2one('stock.location', string='Locations',
        domain="[('usage', 'in', ['internal', 'transit'])]")
    inventory_date = fields.Datetime('Inventory Date',default=fields.Datetime.now)
    binary_file = fields.Binary('File',  required=True)
    file_name = fields.Char('File Name', required=True)

    def import_file(self):
        file = base64.b64decode(self.binary_file)
        excel_fileobj = TemporaryFile('wb+')
        excel_fileobj.write(file)
        excel_fileobj.seek(0)

        book = xlrd.open_workbook(file_contents=file)
        sheet = book.sheet_by_index(0)

        product_template_obj = self.env['product.template']
        product_obj = self.env['product.product']
        uom_obj = self.env['uom.uom']
        # inventory_line = self.env['stock.inventory.line']
        # stock_inventory = self.env['stock.inventory']

        def to_str(cell):
            if cell.ctype is xlrd.XL_CELL_NUMBER:
                return str(int(cell.value))
            elif cell.ctype is xlrd. XL_CELL_TEXT:
                return cell.value
            else:
                return ''

        def to_float(cell):
            if cell.ctype is xlrd.XL_CELL_NUMBER:
                return str(cell.value)
            else:
                return 0.0

        count_row = 0
        product_list = []
        for row in sheet.get_rows():
            # no procesar la primera fila por que es el encabezado
            if count_row == 0:
                pass
            else:
                product_name = to_str(row[0])
                # buscar si el producto existe
                product_tmpl = product_template_obj.search([('name', '=', product_name)])
                qty = to_float(row[1])

                product_res = {'tmpl_id': product_tmpl.id, 'qty': qty}
                # si se encuentra el producto por el codigo
                if product_tmpl:
                    product_res['tmpl_id'] = product_tmpl.id
                else:
                    # CREAR PRODUCTO TEMPLATE
                    product_tmpl_id = product_template_obj.create({'name': product_name,
                                                 'type': 'product'})
                    product_res['tmpl_id'] = product_tmpl_id.id

                product_list.append(product_res)
            count_row += 1

        for product in product_list:
            prod = product_obj.search([('product_tmpl_id', '=', product['tmpl_id'])])
            self.change_product_qty(prod.id, self.location_id.id,product['qty'])

    def change_product_qty(self, product_product_id, warehouse_location_id, quantity):
        """ Changes the Product Quantity by creating/editing corresponding quant.
        """
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', self.env.company.id)], limit=1
        )
        # Before creating a new quant, the quand `create` method will check if
        # it exists already. If it does, it'll edit its `inventory_quantity`
        # instead of create a new one.
        inventory = self.env['stock.quant'].with_context(inventory_mode=True).create({
                                                                        'product_id': product_product_id,
                                                                        'location_id': warehouse_location_id,
                                                                        'inventory_quantity': quantity,
                                                                        })
        inventory._apply_inventory()