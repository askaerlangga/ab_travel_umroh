from odoo import api, fields, models

class ReportXlsx(models.AbstractModel):
    _name = 'report.ab_travel_umroh.report_manifest'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Report %s' % obj.name)

        # Style
        text_top_style = workbook.add_format({
            'font_size': 12,
            'bold': True,
            'align': 'center',
            'border': 3,
        })
        text_header_style = workbook.add_format({
            'font_size': 12,
            'bold': True,
            'font_color': 'white',
            'bg_color': 'blue',
            'valign': 'vcenter',
            'align': 'center',
            'border': 3
        })
        text_style = workbook.add_format({
            'font_size': 12,
            'valign': 'vcenter',
            'text_wrap': True,
            'align': 'center',
            'border': 3
        })
        
        sheet.write('C2', 'Manifest', text_top_style)
        sheet.write('D2', obj.name, text_top_style)

        # Header List
        header_manifest_line = [
            'NO',
            'TITLE',
            'GENDER',
            'FULLNAME',
            'TEMPAT LAHIR',
            'TANGGAL LAHIR',
            'NO. PASSPOR',
            'PASSPOR ISSUED',
            'PASSPOR EXPIRED',
            'IMIGRASI',
            'MAHROM',
            'USIA',
            'NIK',
            'ORDER',
            'ROOM TYPE',
            'ROOM LEADER',
            'NO. ROOM',
            'ALAMAT'
        ]

        header_airline_line = [
            'NO',
            'AIRLINE',
            'DEPARTURE DATE',
            'DEPARTURE CITY',
            'ARRIVAL CITY'
        ]

        # Manifest List
        no_list = []
        partner_title_id = []
        jenis_kelamin = []
        nama_passpor = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passpor = []
        tanggal_berlaku = []
        tanggal_expired = []
        imigrasi = []
        partner_mahrom_id = []
        umur = []
        no_ktp = []
        order = []
        tipe_kamar = []
        room_leader = []
        no_room = []
        city = []

        # Airline List
        no_list2 = []
        airline = []
        tanggal_berangkat = []
        kota_asal= []
        kota_tujuan = []

        # First Row
        row_manifest = 4
        row_airline = 6

        for rec in obj:
            # Numbering
            for i in range(len(rec.manifest_line)):
                no_list.append(i+1)
                row_airline += 1

            for i in range(len(rec.airline_line)):
                no_list2.append(i+1)
            
            # Value
            for ml in rec.manifest_line:
                partner_title_id.append(ml.partner_title_id.name)
                jenis_kelamin.append(ml.jenis_kelamin)
                nama_passpor.append(ml.nama_passpor)
                tempat_lahir.append(ml.tempat_lahir)
                tanggal_lahir.append(ml.tanggal_lahir.strftime('%d-%m-%Y'))
                no_passpor.append(ml.no_passpor)
                tanggal_berlaku.append(ml.tanggal_berlaku.strftime('%d-%m-%Y'))
                tanggal_expired.append(ml.tanggal_expired.strftime('%d-%m-%Y'))
                imigrasi.append(ml.imigrasi)
                partner_mahrom_id.append(ml.partner_mahrom_id.name or '-')
                umur.append(ml.umur)
                no_ktp.append(ml.partner_jamaah_id.no_ktp)
                sale = self.env['sale.order'].search(
                    [('travel_id', '=', obj.id),('manifest_line.partner_jamaah_id.id', '=', ml.partner_jamaah_id.id)])
                order.append(sale.name)
                tipe_kamar.append(ml.tipe_kamar)
                room_leader.append('-')
                no_room.append('-')
                city.append(ml.partner_jamaah_id.city)


            for al in rec.airline_line:
                airline.append(al.partner_id.name)
                tanggal_berangkat.append(al.tanggal_berangkat.strftime('%d-%m-%Y'))
                kota_asal.append(al.kota_asal)
                kota_tujuan.append(al.kota_tujuan)

        # Column size
        sheet.set_column('B:C', 20)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:R', 20)

        # Header
        sheet.write_row('A4', header_manifest_line, text_header_style)
        sheet.write_row(f'C{row_airline}',header_airline_line, text_header_style)

        # Manifest Line
        sheet.write_column(row_manifest, 0, no_list, text_style)
        sheet.write_column(row_manifest, 1, partner_title_id, text_style)
        sheet.write_column(row_manifest, 2, jenis_kelamin, text_style)
        sheet.write_column(row_manifest, 3, nama_passpor, text_style)
        sheet.write_column(row_manifest, 4, tempat_lahir, text_style)
        sheet.write_column(row_manifest, 5, tanggal_lahir, text_style)
        sheet.write_column(row_manifest, 6, no_passpor, text_style)
        sheet.write_column(row_manifest, 7, tanggal_berlaku, text_style)
        sheet.write_column(row_manifest, 8, tanggal_expired, text_style)
        sheet.write_column(row_manifest, 9, imigrasi, text_style)
        sheet.write_column(row_manifest, 10, partner_mahrom_id, text_style)
        sheet.write_column(row_manifest, 11, umur, text_style)
        sheet.write_column(row_manifest, 12, no_ktp, text_style)
        sheet.write_column(row_manifest, 13, order, text_style)
        sheet.write_column(row_manifest, 14, tipe_kamar, text_style)
        sheet.write_column(row_manifest, 15, room_leader, text_style)
        sheet.write_column(row_manifest, 16, no_room, text_style)
        sheet.write_column(row_manifest, 17, city, text_style)
        
        # Airplane Line
        sheet.write_column(row_airline, 2, no_list2, text_style)
        sheet.write_column(row_airline, 3, airline, text_style)
        sheet.write_column(row_airline, 4, tanggal_berangkat, text_style)
        sheet.write_column(row_airline, 5, kota_asal, text_style)
        sheet.write_column(row_airline, 6, kota_tujuan, text_style)
