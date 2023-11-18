# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Data(models.Model):
    _name = 'inventory.data'
    _description = 'Deskripsi Data'

    # name = fields.Char(string="Nama", required=True)
    # color = fields.Selection(selection=[
    #     ('0', 'Merah'), ('1', 'Kuning'), ('2', 'Hijau'), ('3', 'Biru'), ('4', 'Ungu'), 
    # ], string="Warna", required=True)
    # type = fields.Char(string="Jenis", required=True)
    timestamp = fields.Datetime(string="Waktu", default=fields.Datetime.now)
    type = fields.Char(string="Tipe data")
    message = fields.Char(string="Pesan")

class Makanan(models.Model):
    _name = 'inventory.data.makanan'
    _description = 'Deskripsi Makanan'


    name = fields.Char(string="Nama", required=True)
    color = fields.Selection(selection=[
        ('0', 'Merah'), ('1', 'Kuning'), ('2', 'Hijau'), ('3', 'Biru'), ('4', 'Ungu'), 
    ], string="Warna", required=True)
    type = fields.Char(string="Jenis", required=True)

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'name': values.get('name'),
            'color': values.get('color'),
            'type': values.get('type'),
        })
        return super(Makanan, self).create(values)

class Ketersediaan_Bahan(models.Model):
    _name = 'inventory.data.ketersediaan_bahan'
    _description = 'Deskripsi Ketersediaan Bahan'


    name = fields.Char(string="Nama", required=True)
    color = fields.Selection(selection=[
        ('0', 'Merah'), ('1', 'Kuning'), ('2', 'Hijau'), ('3', 'Biru'), ('4', 'Ungu'), 
    ], string="Warna", required=True)
    type = fields.Char(string="Jenis", required=True)

    @api.model
    def create(self, values):
        self.env['inventory.data'].create({
            'name': values.get('name'),
            'color': values.get('color'),
            'type': values.get('type'),
        })
        return super(Ketersediaan_Bahan, self).create(values)

class Pembelian_Bahan_Mentah(models.Model):
    _name = 'inventory.data.pembelian_bahan_mentah'
    _description = 'Deskripsi Pembelian Bahan Mentah'


    supplier = fields.Char(string="Pemasok", required=True)
    date = fields.Date(string="Date")
    name = fields.Char(string="Makanan")
    quantity = fields.Integer(string="Jumlah", default=1)
    message = fields.Char(string="Keterangan")

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


    name = fields.Char(string="Makanan")
    quantity = fields.Integer(string="Jumlah", default=1)
    date = fields.Date(string="Date")
    message = fields.Char(string="Keterangan")

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



