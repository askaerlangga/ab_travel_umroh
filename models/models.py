# -*- coding: utf-8 -*-
from unicodedata import name
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

class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'
    
    # Informasi Jadwal
    tanggal_berangkat = fields.Date('Tanggal berangkat', required=True)
    tanggal_kembali = fields.Date('Tanggal Kembali', required=True)
    
    # Produk
    product_sale_id = fields.Many2one('product.product', string='Sale', required=True)
    product_package_id = fields.Many2one('product.product', string='Package', required=True)

    # Seats
    quota = fields.Integer('Quota')
    remaining_quota = fields.Integer('Remaining Quota')
    quota_progress = fields.Float('Quota Progress')

    # Lines
    hotels_line = fields.One2many('hotels.lines', 'travel_id', string='Hotels Line')
    airline_line = fields.One2many('airline.lines', 'travel_id', string='Airline Lines')
    schedule_line = fields.One2many('schedule.lines', 'travel_id', string='Schedule Lines')
    manifest_line = fields.One2many('manifest.lines', 'travel_id', string='Manifest Lines')
    hpp_line = fields.One2many('hpp.lines', 'travel_id', string='HPP Lines')

    total = fields.Float(compute='_compute_total', string='Total')

    # Sequence Travel Package
    name = fields.Char(string='Referensi', readonly=True, default='/')
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)

     # Onchange Quota
    @api.onchange('quota')
    def _onchange_quota(self):
        self.remaining_quota = self.quota

    # Compute Total
    @api.depends('hpp_line.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = 0
            for i in rec.hpp_line:
                print('PRINT ==============>',i.subtotal)
                rec.total += i.subtotal
                print('TOTAL : ', rec.total)

    # Onchange Package
    @api.onchange('product_package_id')
    def _onchange_product_package_id(self):
        for rec in self:
            lines = [(5,0,0)]
            for line in rec.product_package_id.bom_ids.bom_line_ids:
                vals = {
                    'travel_id' : line.id,
                    'barang' : line.display_name,
                    'quantity' : line.product_qty,
                    'unit' : line.product_uom_id.id,
                    'unit_price' : line.product_id.standard_price,
                }
                lines.append((0, 0, vals))
            rec.hpp_line = lines

class HotelsLines(models.Model):
    _name = 'hotels.lines'
    _description = 'Hotels Lines'

    travel_id = fields.Many2one('travel.package', string='Hotels Lines')
    partner_id = fields.Many2one('res.partner', string='Nama Hotel', required=True, domain=[('hotels', '=', True)])
    check_in = fields.Date('Check In Hotel', required=True)
    check_out = fields.Date('Check Out Hotel', required=True)
    kota = fields.Char(string='Kota', related='partner_id.city')

class AirlineLines(models.Model):
    _name = 'airline.lines'
    _description = 'Airline Lines'

    travel_id = fields.Many2one('travel.package', string='Airline Lines')
    partner_id = fields.Many2one('res.partner', string='Nama Airline', required=True, domain=[('airlines', '=', True)])
    tanggal_berangkat = fields.Date('Tanggal Berangkat', required=True)
    kota_asal = fields.Char('Kota Asal', required=True)
    kota_tujuan = fields.Char('Kota Tujuan', required=True)

class ScheduleLines(models.Model):
    _name = 'schedule.lines'
    _description = 'Schedule Lines'

    travel_id = fields.Many2one('travel.package', string='Schedule Lines')
    schedule_name = fields.Char(string='Nama Kegiatan',required=True)
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan', required=True)

class ManifestLines(models.Model):
    _name = 'manifest.lines'
    _description = 'Manifest Lines'

    travel_id = fields.Many2one('travel.package', string='Manifest Lines')
    title = fields.Char('Title')
    nama_passpor = fields.Char('Nama Passpor')
    jenis_kelamin = fields.Char('Jenis Kelamin')
    no_ktp = fields.Char('No. KTP')
    no_passpor = fields.Char('No. Passpor')
    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    tempat_lahir = fields.Char('Tempat Lahir')
    tanggal_berlaku = fields.Date('Tanggal Berlaku')
    tanggal_expired = fields.Date('Tanggal Expired')
    imigrasi = fields.Char('Imigrasi')
    tipe_kamar = fields.Char('Tipe Kamar')
    umur = fields.Integer('Umur')
    mahrom = fields.Char('Mahrom')
    agent = fields.Char('Agent')

class HPPLines(models.Model):
    _name = 'hpp.lines'
    _description = 'HPP Lines'

    travel_id = fields.Many2one('travel.package', string='HPP Lines')
    barang = fields.Char('Barang')
    quantity = fields.Integer('Quantity')
    unit = fields.Many2one('uom.uom', string='Unit(s)')
    unit_price = fields.Float('Unit Price')
    subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal')
    
    # Compute Subtotal
    @api.depends('quantity')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = 0
            if rec.quantity and rec.unit_price:
                rec.subtotal = rec.quantity * rec.unit_price