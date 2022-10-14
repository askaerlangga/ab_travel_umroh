# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Additional Information
    no_ktp = fields.Char('No. KTP')
    nama_ayah = fields.Char('Nama Ayah')
    pekerjaan_ayah = fields.Char('Pekerjaan Ayah')
    tempat_lahir = fields.Char('Tempat Lahir')
    pendidikan = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('diploma', 'Diploma'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3')
    ], string='Pendidikan')
    status_hubungan = fields.Selection([
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorce', 'Divorce')
    ], string='Status Hubungan')
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin')
    nama_ibu = fields.Char('Nama Ibu')
    pekerjaan_ibu = fields.Char('Pekerjaan Ibu')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    golongan_darah = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ], string='Golongan Darah')
    ukuran_baju = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('xxxxl', 'XXXXL'),
    ], string='Ukuran Baju')

    # Passpor Information
    no_passpor = fields.Char('No. Passpor')
    tanggal_berlaku = fields.Date('Tanggal Berlaku')
    imigrasi = fields.Char('Imigrasi')
    nama_passpor = fields.Char('Nama Passpor')
    tanggal_expired = fields.Date('Tanggal Expired')

    # Scan Document
    scan_passpor = fields.Image('Scan Passpor')
    scan_ktp = fields.Image('Scan KTP')
    scan_buku_nikah = fields.Image('Scan Buku Nikah')
    scan_kartu_keluarga = fields.Image('Scan Kartu Keluarga')

    # Travel
    hotels = fields.Boolean('Hotels')
    airlines = fields.Boolean('Airlines')

    tanggal_berangkat = fields.Date('Tanggal berangkat')
    tanggal_kembali = fields.Date('Tanggal Kembali', required=True)
    sale_id = fields.Many2one('product.product', string='Sale')
    kota_id = fields.Many2one('res.partner', string='Kota')
    package_id = fields.Many2one('product.product', string='Package')
    quota = fields.Integer('Quota')
    remaining_quota = fields.Integer('Remaining Quota')
    quota_progress = fields.Float('Quota Progress')
    hotels_line = fields.One2many('hotels.lines', 'hotels_id', string='Hotels')


class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'

    @api.onchange('quota')
    def _onchange_quota(self):
        self.remaining_quota = self.quota

    tanggal_berangkat = fields.Date('Tanggal berangkat', required=True)
    tanggal_kembali = fields.Date('Tanggal Kembali', required=True)
    
    sale_id = fields.Many2one('product.product', string='Sale')
    package_id = fields.Many2one('product.product', string='Package')

    quota = fields.Integer('Quota')
    remaining_quota = fields.Integer('Remaining Quota')
    quota_progress = fields.Float('Quota Progress')

    hotels_line = fields.One2many('hotels.lines', 'hotels_id', string='Hotels')


class HotelLines(models.Model):
    _name = 'hotels.lines'

    hotels_id = fields.Many2one('res.partner', string='Nama Hotel', required=True, domain=[('hotels', '=', True)])
    check_in = fields.Date('Check In Hotel', required=True)
    check_out = fields.Date('Check Out Hotel', required=True)
    kota_id = fields.Many2one('res.partner', string='Kota')
    # kota_id = fields.Many2one('res.city', string='Kota', related='hotels_id.city')

    @api.onchange('hotels_id')
    def _onchange_hotels_id(self):
        pass