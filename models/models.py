# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class Data(models.Model):
    _name = 'inventory.data'
    _description = 'Deskripsi Data'

    timestamp = fields.Datetime(string="Waktu", default=fields.Datetime.now)
    action = fields.Char(string="Aksi")
    type = fields.Char(string="Tipe data")
    # message = fields.Text(string="Pesan")
    name = fields.Char(string="Nama Makanan")

class Makanan(models.Model):
    _name = 'inventory.data.makanan'
    _description = 'Deskripsi Makanan'


    name = fields.Char(string="Nama", required=True, unique=True)
    expired = fields.Integer(string="Lama Kadaluarsa(Hari)", default=1, required=True)
    price = fields.Monetary(string="Harga(Rp)", required=True, currency_field='currency_id')
    recipe = fields.Text(string="Resep", required=True)
    type = fields.Selection(selection=[
        ('0', 'Data Bahan Mentah'), ('1', 'Data Bahan Setengah Matang'), ('2', 'Data Makanan Siap Saji') 
    ], string="Tipe Makanan", required=True, create=False)
    unit = fields.Selection(selection=[
        ('0', 'Kilogram'), ('1', 'Gram'), ('2', 'Buah') ,('3', 'Siung') 
    ], string="Satuan", required=True)
    # message = fields.Text(string="Pesan")

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1),
        readonly=True,
    )

    @api.onchange('type')
    def onchange_type(self):

        if self.type and self.type in ['0']:
            self.recipe = "-"
        elif self.type and self.type in ['1']:
            self.price = 0
        
        if self.type and self.type in ['2']:
            self.unit = '2'
    
    @api.onchange('recipe')
    def onchange_recipe(self):

        if self.recipe != "-" and self.type in ['0']:
            self.recipe = "-"

    @api.onchange('price')
    def onchange_price(self):

        if self.price != 0 and self.type in ['1']:
            self.price = 0
    
    @api.onchange('unit')
    def onchange_unit(self):

        if self.type in ['2'] and self.unit not in ['2']:
            self.unit = '2'

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Create",
            'type': "Makanan",
            # 'message': values.get('message'),
            'name': values.get('name')
        })
        return super(Makanan, self).create(values)
    
    
    def write(self, values):
        name = values.get('name', self.name)

        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Update",
            'type': "Makanan",
            # 'message': values.get('message'),
            'name': name
        })

        res = super(Makanan, self).write(values)

        return res
    
    
    def unlink(self):
        for record in self:
            self.env['inventory.data'].create({
                'timestamp': datetime.now(),
                'action': "Delete",
                'type': "Makanan",
                'name': record.name
                
            })

        res = super(Makanan, self).unlink()

        return res

class Ketersediaan_Bahan(models.Model):
    _name = 'inventory.data.ketersediaan_bahan'
    _description = 'Deskripsi Ketersediaan Bahan'

    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', 'in', ['0', '1'])], required=True, ondelete='cascade')
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    unit = fields.Char(string="Satuan", required=True)
    storage = fields.Char(string="Tempat Penyimpanan", required=True)
    # expire_date = fields.Date(string="Tanggal", required=True)
    # message = fields.Text(string="Pesan")
    expire_date = fields.Date(string="Tanggal", compute='_compute_expire_date', store=True, readonly=True)

    @api.depends('name', 'name.expired')
    def _compute_expire_date(self):
        for record in self:
            if not record._origin:
                if record.name and record.name.expired:
                    expire_date = fields.Date.from_string(fields.Date.today()) + timedelta(days=record.name.expired)
                    record.expire_date = fields.Date.to_string(expire_date)
                else:
                    record.expire_date = False
            elif not record.expire_date:
                if record.name and record.name.expired:
                    expire_date = fields.Date.from_string(fields.Date.today()) + timedelta(days=record.name.expired)
                    record.expire_date = fields.Date.to_string(expire_date)
                else:
                    record.expire_date = False
    

    @api.onchange('name')
    def onchange_name(self):

        if self.name and self.name.type not in ['0', '1']:
            self.name = False

        if self.name:
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    @api.onchange('unit')
    def onchange_unit(self):
        if self.name and self.unit != dict(self.name._fields['unit'].selection).get(self.name.unit, False):
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)

    @api.model
    def create(self, values):
        name = self.env['inventory.data.makanan'].browse(values.get('name')).name
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Create",
            'type': "Ketersediaan Bahan",
            # 'message': values.get('message'),
            'name': name
        })
        return super(Ketersediaan_Bahan, self).create(values)
    
    
    def write(self, values):

        name = self.env['inventory.data.makanan'].browse(values.get('name')).name if values.get('name') and values.get('name') != self.name.id else self.name.name

        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Update",
            'type': "Ketersediaan Bahan",
            # 'message': values.get('message'),
            'name': name
        })

        res = super(Ketersediaan_Bahan, self).write(values)

        return res
    
    
    def unlink(self):
        for record in self:
            name = self.env['inventory.data.makanan'].browse(record.name.id).name
            self.env['inventory.data'].create({
                'timestamp': datetime.now(),
                'action': "Delete",
                'type': "Ketersediaan Bahan",
                'name': name
                
            })

        res = super(Ketersediaan_Bahan, self).unlink()

        return res

class Pembelian_Bahan_Mentah(models.Model):
    _name = 'inventory.data.pembelian_bahan_mentah'
    _description = 'Deskripsi Pembelian Bahan Mentah'


    supplier = fields.Char(string="Pemasok", required=True)
    date = fields.Date(string="Tanggal", required=True)
    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', '=', '0')], required=True, ondelete='cascade')
    unit = fields.Char(string="Satuan", required=True)
    price = fields.Monetary(string="Harga(Rp)", required=True, currency_field='currency_id')
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    # message = fields.Text(string="Pesan")

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1),
        readonly=True,
    )

    @api.onchange('name')
    def onchange_name(self):
        if self.name and self.name.type not in ['0']:
            self.name = False

        if self.name:
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
            self.price = self.name.price
    
    @api.onchange('unit')
    def onchange_unit(self):
        if self.name and self.unit != dict(self.name._fields['unit'].selection).get(self.name.unit, False):
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    @api.onchange('price')
    def onchange_price(self):
        if self.name and self.price != self.name.price:
            self.price = self.name.price

    @api.model
    def create(self, values):
        name = self.env['inventory.data.makanan'].browse(values.get('name')).name
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Create",
            'type': "Pembelian bahan mentah",
            # 'message': values.get('message'),
            'name': name

        })
        return super(Pembelian_Bahan_Mentah, self).create(values)

    
    def write(self, values):

        name = self.env['inventory.data.makanan'].browse(values.get('name')).name if values.get('name') and values.get('name') != self.name.id else self.name.name

        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Update",
            'type': "Pembelian bahan mentah",
            # 'message': values.get('message'),
            'name': name
        })

        res = super(Pembelian_Bahan_Mentah, self).write(values)

        return res
    
    
    def unlink(self):
        for record in self:
            name = self.env['inventory.data.makanan'].browse(record.name.id).name
            self.env['inventory.data'].create({
                'timestamp': datetime.now(),
                'action': "Delete",
                'type': "Pembelian bahan mentah",
                'name': name
                
            })

        res = super(Pembelian_Bahan_Mentah, self).unlink()

        return res

class Produksi_Makanan_Siap_Saji(models.Model):
    _name = 'inventory.data.produksi_makanan_siap_saji'
    _description = 'Deskripsi Produksi Makanan Siap Saji'


    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', '=', '2')], required=True, ondelete='cascade')
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    # unit = fields.Char(string="Satuan", required=True)
    unit = fields.Char(string="Satuan", default="Buah", readonly= True, required=True)
    price = fields.Monetary(string="Harga(Rp)", required=True, currency_field='currency_id')
    date = fields.Date(string="Tanggal", required=True)
    # message = fields.Char(string="Pesan")

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1),
        readonly=True,
    )

    @api.onchange('name')
    def onchange_name(self):
        if self.name and self.name.type not in ['2']:
            self.name = False
        
        if self.name:
            self.price = self.name.price

        # if self.name:
        #     self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    # @api.onchange('unit')
    # def onchange_unit(self):
    #     if self.name and self.unit != dict(self._fields['unit'].selection).get(self.name.unit, False):
    #         self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)

    @api.onchange('price')
    def onchange_price(self):
        if self.name and self.price != self.name.price:
            self.price = self.name.price

    @api.model
    def create(self, values):
        name = self.env['inventory.data.makanan'].browse(values.get('name')).name
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Create",
            'type': "Produksi Makanan Siap Saji",
            # 'message': values.get('message'),
            'name': name
        })
        return super(Produksi_Makanan_Siap_Saji, self).create(values)
    
    
    def write(self, values):

        name = self.env['inventory.data.makanan'].browse(values.get('name')).name if values.get('name') and values.get('name') != self.name.id else self.name.name

        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'action': "Update",
            'type': "Produksi Makanan Siap Saji",
            # 'message': values.get('message'),
            'name': name
        })

        res = super(Produksi_Makanan_Siap_Saji, self).write(values)

        return res
    
    
    def unlink(self):
        for record in self:
            name = self.env['inventory.data.makanan'].browse(record.name.id).name
            self.env['inventory.data'].create({
                'timestamp': datetime.now(),
                'action': "Delete",
                'type': "Produksi Makanan Siap Saji",
                'name': name
                
            })

        res = super(Produksi_Makanan_Siap_Saji, self).unlink()

        return res

class Report(models.Model):
    _name = 'inventory.report'
    _description = 'Laporan Pergudangan'


    name = fields.Char(string="Nama")



