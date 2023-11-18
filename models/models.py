# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Data(models.Model):
    _name = 'inventory.data'
    _description = 'Deskripsi Data'

    timestamp = fields.Datetime(string="Waktu", default=fields.Datetime.now)
    type = fields.Char(string="Tipe data")
    message = fields.Text(string="Pesan")

class Makanan(models.Model):
    _name = 'inventory.data.makanan'
    _description = 'Deskripsi Makanan'


    name = fields.Char(string="Nama", required=True)
    expired = fields.Integer(string="Lama Kadaluarsa(Hari)", default=1, required=True)
    price = fields.Monetary(string="Harga(Rp)", required=True, default=1000, currency_field='currency_id')
    recipe = fields.Text(string="Resep", required=True)
    type = fields.Selection(selection=[
        ('0', 'Data Bahan Mentah'), ('1', 'Data Bahan Setengah Matang'), ('2', 'Data Makanan Siap Saji') 
    ], string="Tipe Makanan", required=True, create=False)
    unit = fields.Selection(selection=[
        ('0', 'Kilogram'), ('1', 'Gram'), ('2', 'Buah') ,('3', 'Siung') 
    ], string="Satuan", required=True)
    message = fields.Text(string="Pesan")

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1),
        readonly=True,
    )

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'type': "Makanan",
            'message': values.get('message'),
        })
        return super(Makanan, self).create(values)

class Ketersediaan_Bahan(models.Model):
    _name = 'inventory.data.ketersediaan_bahan'
    _description = 'Deskripsi Ketersediaan Bahan'

    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', 'in', ['0', '1'])], required=True)
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    unit = fields.Char(string="Satuan", required=True)
    storage = fields.Char(string="Tempat Penyimpanan", required=True)
    expire_date = fields.Date(string="Tanggal", required=True)
    message = fields.Text(string="Pesan")

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    @api.onchange('unit')
    def onchange_unit(self):
        if self.name and self.unit != dict(self.name._fields['unit'].selection).get(self.name.unit, False):
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'type': "Ketersediaan Bahan",
            'message': values.get('message'),
        })
        return super(Ketersediaan_Bahan, self).create(values)

class Pembelian_Bahan_Mentah(models.Model):
    _name = 'inventory.data.pembelian_bahan_mentah'
    _description = 'Deskripsi Pembelian Bahan Mentah'


    supplier = fields.Char(string="Pemasok", required=True)
    date = fields.Date(string="Tanggal", required=True)
    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', '=', '0')], required=True)
    unit = fields.Char(string="Satuan", required=True)
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    message = fields.Text(string="Pesan")

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    @api.onchange('unit')
    def onchange_unit(self):
        if self.name and self.unit != dict(self.name._fields['unit'].selection).get(self.name.unit, False):
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'type': "Pembelian bahan mentah",
            'message': values.get('message'),
        })
        return super(Pembelian_Bahan_Mentah, self).create(values)

class Produksi_Makanan_Siap_Saji(models.Model):
    _name = 'inventory.data.produksi_makanan_siap_saji'
    _description = 'Deskripsi Produksi Makanan Siap Saji'


    name = fields.Many2one('inventory.data.makanan', string="Makanan", domain=[('type', '=', '2')], required=True)
    quantity = fields.Integer(string="Jumlah", default=1, required=True)
    unit = fields.Char(string="Satuan", required=True)
    date = fields.Date(string="Tanggal", required=True)
    message = fields.Char(string="Pesan")

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)
    
    @api.onchange('unit')
    def onchange_unit(self):
        if self.name and self.unit != dict(self._fields['unit'].selection).get(self.name.unit, False):
            self.unit = dict(self.name._fields['unit'].selection).get(self.name.unit, False)

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'timestamp': datetime.now(),
            'type': "Produksi Makanan Siap Saji",
            'message': values.get('message'),
        })
        return super(Produksi_Makanan_Siap_Saji, self).create(values)

class Report(models.Model):
    _name = 'inventory.report'
    _description = 'Laporan Pergudangan'


    name = fields.Char(string="Nama")



