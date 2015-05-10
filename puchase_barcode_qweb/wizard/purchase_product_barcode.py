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

import time
from openerp.osv import osv, fields

import logging
_logger = logging.getLogger(__name__)

class purchase_product_barcode_print(osv.osv_memory):
    _name = 'purchase.product.barcode.print'
    _description = 'Product Barcode Print'

    _columns = {
        'product_ids': fields.many2many('purchase.product.barcode.lines', 'purchase_product_barcode_print_product_product_rel', 'product_id', 'wizard_id', 'Products to print labels'),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        line_obj = self.pool.get('purchase.product.barcode.lines')
        res = super(purchase_product_barcode_print, self).default_get(cr, uid, fields, context=context)
        if context.get('active_id'):
            purchase = self.pool.get('purchase.order').browse(cr, uid, context.get('active_id'), context=context)
            res.update({'product_ids':[(6, 0, [line_obj.create(cr, uid, {'product_id':x.product_id.id , 'qty':x.product_qty}) for x in purchase.order_line if x.product_id])]})
        return res

    def print_report(self, cr, uid, ids, context=None):
        """
         To get the parameters and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return : retrun report
        """
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        if ids:
            res = self.read(cr, uid, ids, ['product_ids'], context=context)
            res = res and res[0] or {}
            prod_details = [{'product_id':x.product_id.id, 'qty':x.qty} for x in self.browse(cr, uid, ids[0], context=context).product_ids]
            datas.update({'form':res, 'prod_details':prod_details , 'ids':ids})
            _logger.warning(datas)

            return self.pool['report'].get_action(cr, uid, [], 'purchase_barcode_qweb.report_purchase_barcode', data=datas, context=context)
        return True

class purchase_product_barcode_lines(osv.osv_memory):
    _name = 'purchase.product.barcode.lines'

    _columns = {
        'product_id': fields.many2one('product.product', 'Product to print label'),
        'qty': fields.integer('Number of labels', help='How many labels to print'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
