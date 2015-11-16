# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more summary.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

#from barcode.writer import ImageWriter
#from barcode import generate
from Code128 import Code128
import base64
from StringIO import StringIO

import time
import math
from openerp.osv import osv
from openerp.report import report_sxw


class purchase_barcode_print(report_sxw.rml_parse):

    def _getLabelRows(self, data, context=None):
        context = self.context
        form = data['form']
        product_obj = self.pool.get('product.product')
        result_data = []
        result = {}
        product_ids = data['form']['product_ids']
        if not product_ids:
            return {}
        for product in data['prod_details']:
            product_id = product['product_id']
            if not product_id:
                continue
            product_read = product_obj.read(self.cr, self.uid, [product_id],
                                            ['name', 'default_code', 'list_price'])[0]
            qty = product['qty']
            for product_row in range(int(math.ceil(float(qty)/1))):
                label_row=[]
                for row in [1]:
                    label_data = {
                        'name': product_read['name'],
                        'default_code': product_read['default_code'],
                        'price': product_read['list_price'],
                    }
                    label_row.append(label_data)
                result_data.append(label_row)

        if result_data:
            return result_data
        else:
            return {}

    def _generateBarcode(self, barcode_string):  #, height, width):
        fp = StringIO()
        #generate('CODE39', barcode_string, writer=ImageWriter(), add_checksum=False, output=fp)
        #barcode_data = base64.b64encode(fp.getvalue())
        #return '<img style="width: 25mm;height: 7mm;" src="data:image/png;base64,%s" />'%(barcode_data)
        #return barcode_data
        Code128().getImage(barcode_string, path="./").save(fp, "PNG")
        barcode_data = base64.b64encode(fp.getvalue())
        return barcode_data

    def __init__(self, cr, uid, name, context):
        super(purchase_barcode_print, self).__init__(cr, uid, name, context=context)
        self.total = 0.0
        self.qty = 0.0
        self.total_invoiced = 0.0
        self.discount = 0.0
        self.total_discount = 0.0
        self.context = context
        self.localcontext.update({
            'time': time,
            'getLabelRows':self._getLabelRows,
            'generateBarcode':self._generateBarcode,
        })


class report_purchase_barcode_print(osv.AbstractModel):
    _name = 'report.purchase_barcode_qweb.report_purchase_barcode'
    _inherit = 'report.abstract_report'
    _template = 'purchase_barcode_qweb.report_purchase_barcode'
    _wrapped_report_class = purchase_barcode_print

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
