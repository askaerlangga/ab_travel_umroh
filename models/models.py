# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelUmroh(models.Model):
    _name = 'travel.umroh'
    _description = 'Travel Umroh'

    name = fields.Char(string='Judul', required=True)
    description = fields.Text(string='Keterangan')
    

class TravelUmrohPartner(models.Model):
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
    scan_passpor = fields.Binary('Scan Passpor')
    scan_ktp = fields.Binary('Scan KTP')
    scan_buku_nikah = fields.Binary('Scan Buku Nikah')
    scan_kartu_keluarga = fields.Binary('Scan Kartu Keluarga')
