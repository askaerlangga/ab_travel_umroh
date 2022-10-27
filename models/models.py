# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date
import json

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
    tanggal_berangkat = fields.Date('Tanggal berangkat', required=True, readonly=True, states={'draft': [('readonly', False)]})
    tanggal_kembali = fields.Date('Tanggal Kembali', required=True, readonly=True, states={'draft': [('readonly', False)]})
    
    # Produk
    product_sale_id = fields.Many2one('product.product', string='Sale', required=True, readonly=True, states={'draft': [('readonly', False)]})
    product_package_id = fields.Many2one('product.product', string='Package', required=True, readonly=True, states={'draft': [('readonly', False)]})

    # Seats
    quota = fields.Integer('Quota', readonly=True, states={'draft': [('readonly', False)]})
    remaining_quota = fields.Integer(
        compute='_compute_remaining_quota', string='Remaining Quota')
    quota_progress = fields.Float('Quota Progress')

    # Lines
    hotels_line = fields.One2many('hotels.lines', 'travel_id', string='Hotels Line', readonly=True, states={'draft': [('readonly', False)]})
    airline_line = fields.One2many('airline.lines', 'travel_id', string='Airline Lines', readonly=True, states={'draft': [('readonly', False)]})
    schedule_line = fields.One2many('schedule.lines', 'travel_id', string='Schedule Lines', readonly=True, states={'draft': [('readonly', False)]})
    manifest_line = fields.One2many('manifest.lines', 'travel_id', string='Manifest Lines', readonly=True, states={'draft': [('readonly', False)]})
    hpp_line = fields.One2many('hpp.lines', 'travel_id', string='HPP Lines', readonly=True, states={'draft': [('readonly', False)]})

    total = fields.Float(compute='_compute_total', string='Total')

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')], string='Status', readonly=True, default='draft')

    # Sequence Travel Package
    name = fields.Char(string='Referensi', readonly=True, default='/')
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)
    
    # Compute Remaining Quota
    @api.depends('quota')
    def _compute_remaining_quota(self):
        for rec in self:
            rec.remaining_quota = rec.quota
            if len(rec.manifest_line) > 0: rec.remaining_quota -= len(rec.manifest_line)

    # Compute Total
    @api.depends('hpp_line.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total = 0
            for i in rec.hpp_line:
                rec.total += i.subtotal

    # Onchange Package
    @api.onchange('product_package_id')
    def _onchange_product_package_id(self):
        for rec in self:
            lines = [(5,0,0)]
            for line in rec.product_package_id.bom_ids.bom_line_ids:
                vals = {
                    'barang' : line.display_name,
                    'quantity' : line.product_qty,
                    'unit' : line.product_uom_id.id,
                    'unit_price' : line.product_id.standard_price,
                }
                lines.append((0, 0, vals))
            rec.hpp_line = lines

    # Action State
    def action_confirm(self):
        self.write({'state': 'confirm'})
      
    def action_cancel(self):
        self.write({'state': 'draft'})
      
    def action_close(self):
        self.write({'state': 'done'})

    # Button Update jamaah
    def action_update_jamaah(self):
        for rec in self:
            rec.manifest_line.unlink()
            order = self.env['sale.order'].search([('travel_id', '=', self.id), ('state', 'in', ('sale','done'))])
            for sale in order:
                for line in sale.manifest_line:
                    self.manifest_line.create({
                        'partner_jamaah_id':line.partner_jamaah_id.id,
                        'partner_mahrom_id': line.partner_mahrom_id.id,
                        'tipe_kamar' : line.tipe_kamar,
                        'travel_id': rec.id
                    })

            rec.quota_progress = ((rec.quota - rec.remaining_quota) / rec.quota) * 100

    # Print Manifest XLSX
    def action_print_manifest(self):
        return self.env.ref('ab_travel_umroh.report_travel_package_action').report_action(self)

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
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    
    # Personal
    partner_jamaah_id = fields.Many2one('res.partner', string='Nama Jamaah')
    partner_title_id = fields.Many2one(
        'res.partner.title', string='Title', related='partner_jamaah_id.title')
    tipe_kamar = fields.Selection([
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad')
    ], string='Tipe kamar',)
    tanggal_lahir = fields.Date(
        'Tanggal Lahir', related='partner_jamaah_id.tanggal_lahir')
    no_ktp = fields.Char('No. KTP', related='partner_jamaah_id.no_ktp')
    partner_mahrom_id = fields.Many2one('res.partner', string='Mahrom')
    umur = fields.Integer(compute='_compute_umur', string='Umur')

    tempat_lahir = fields.Char(
        'Tempat Lahir', related='partner_jamaah_id.tempat_lahir')

    # Passport
    no_passpor = fields.Char('No. Passpor', related='partner_jamaah_id.no_passpor')
    tanggal_berlaku = fields.Date(
        'Tanggal Berlaku', related='partner_jamaah_id.tanggal_berlaku')
    imigrasi = fields.Char('Imigrasi', related='partner_jamaah_id.imigrasi')
    nama_passpor = fields.Char(
        'Nama Passpor', related='partner_jamaah_id.nama_passpor')
    tanggal_expired = fields.Date(
        'Tanggal Expired', related='partner_jamaah_id.tanggal_expired')
    notes = fields.Char('Notes')

    # Scan Document
    scan_passpor = fields.Image('Scan Passpor')
    scan_ktp = fields.Image('Scan KTP')
    scan_buku_nikah = fields.Image('Scan Buku Nikah')
    scan_kartu_keluarga = fields.Image('Scan Kartu Keluarga')

    jenis_kelamin = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin', related='partner_jamaah_id.jenis_kelamin')
    agent = fields.Char('Agent')
    user_id = fields.Many2one(
        'res.users', string='Agent', default=lambda self: self.env.user)
    
    @api.depends('tanggal_lahir')
    def _compute_umur(self):
        for rec in self:
            if rec.tanggal_lahir is not False:
                rec.umur = relativedelta(date.today(),rec.tanggal_lahir).years
            else:
                rec.umur = 0

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

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    travel_id = fields.Many2one('travel.package', string='Paket Perjalanan', domain=[('state', '=', 'confirm')])
    manifest_line = fields.One2many('manifest.lines', 'sale_id', string='Passport Line')

    # Onchange Package
    # @api.onchange('travel_id')
    # def _onchange_travel_id(self):
    #     for rec in self:
    #         lines = [(5,0,0)]
    #         for line in rec.travel_id.product_sale_id:
    #             vals = {
    #                 'product_id' : line.id,
    #                 'name' : line.name,
    #                 'product_uom' : line.uom_id,
    #                 'price_unit' : line.list_price,
    #                 'tax_id' : line.taxes_id,
    #             }
    #             lines.append((0, 0, vals))
    #         rec.order_line = lines

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_print_delivery(self):
        return self.env.ref('ab_travel_umroh.report_delivery_action').report_action(self)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_json_invoice_payment(self):
        data = json.loads(self.invoice_payments_widget)
        if data:
            return data['content']
        return


    def action_print_invoice(self):
        return self.env.ref('ab_travel_umroh.report_invoice_action').report_action(self)
