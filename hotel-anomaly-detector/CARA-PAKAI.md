# Hotel FO Anomaly Detector — Cara Pakai

Aplikasi audit analytics untuk mendeteksi anomali transaksi Front Office hotel.

---

## Fitur

### 1. Rate Change Anomaly
Analisis laporan perubahan tarif kamar dari PMS:
- Rate turun lebih dari 30% (CRITICAL jika >50% atau dilakukan dini hari)
- Rate diturunkan ke hampir nol (< Rp 10.000 dari sebelumnya > Rp 50.000)
- Perubahan rate di jam 22:00 – 06:00
- Rate berubah tanpa Staff ID tercatat
- Satu reservasi berubah rate lebih dari 1x dalam sehari

### 2. FO Transaction Anomaly
Analisis jurnal transaksi FO (pembayaran + pendapatan):
- **Split Payment**: Satu billing mencakup dua kamar/tamu berbeda, dibayar Cash + Non-Cash
- **Bill Chain**: Rantai transfer folio lintas kamar dengan pembayaran tunai
- **Room Consolidation**: Charge kamar digabung ke satu folio, dibayar tepat Card + Cash
- **Tanpa Pembayaran**: Kamar dengan room charge tapi tidak ada pembayaran

---

## Cara Menjalankan

### Mac / Linux
```bash
bash start-mac.sh
```
Buka browser: **http://localhost:5050**

### Windows
Klik dua kali file `start-windows.bat`  
Buka browser: **http://localhost:5050**

---

## Format File yang Didukung

| Format | Keterangan |
|--------|-----------|
| `.numbers` | Apple Numbers — ekspor langsung dari Mac |
| `.xlsx` | Microsoft Excel |
| `.xls` | Excel lama |
| `.csv` | Comma-separated values |

---

## Cara Ekspor dari PMS

### Rate Change Report
- Di PMS (Opera/Realta): Laporan → Perubahan Tarif / Rate Change Log
- Ekspor ke Excel atau Numbers
- Format kolom yang diperlukan (dari kiri): Reservation No, Resv Member No, Status, Arrival, Departure, Night Stay, Room No, Room Type, Rate Code, **Rate Baru**, **Rate Lama**, **Variance**, Guest Name, Reservation Name, **Staff ID (Pengubah)**, **Staff ID (Approver)**, **Tanggal Ubah**, **Jam Ubah**

### FO Transaction Journal (Pembayaran + Pendapatan)
- Di PMS: Laporan → Jurnal Transaksi FO
- Ekspor dua file terpisah:
  - **File Pembayaran**: Article 1–49 (metode pembayaran)
  - **File Pendapatan**: Article 99–100 (room charge)
- Format kolom: Date, Room Number, Non Stay, Master Bill, Shift, Bill Number, Article Number, Description, Payment By, Voucher Number, Department, Outlet, Quantity, Amount, Guest Name, Bill Receiver, Reservation Name, Segment Code, Check-in Date, Check-out Date, Time, ID, System Date, Remark, Nationality, Reservation Number, Source Booking

---

## Cara Membaca Output Excel

File Excel hasil analisis berisi sheet:
- **Ringkasan**: Overview semua temuan dengan severity
- **RC-1 Rate Turun >30%**: Anomali penurunan tarif signifikan
- **RC-2 Rate Hampir Nol**: Tarif diturunkan ekstrem
- **RC-3 Dini Hari**: Perubahan di jam 22:00–06:00
- **RC-4 Tanpa Staff ID**: Rate berubah tanpa pencatat
- **RC-5 Multi Perubahan**: >1x ubah rate dalam sehari
- **FO-1 Split Payment**: Satu billing dua kamar + Cash
- **FO-2 Bill Chain**: Rantai folio lintas kamar + Cash
- **FO-3 Room Konsolidasi**: Gabungan charge dibayar Card+Cash
- **FO-4 Tanpa Bayar**: Room charge tanpa pembayaran

### Kode Warna Severity
| Warna | Severity | Arti |
|-------|----------|------|
| Merah | CRITICAL | Tindak lanjut segera, potensi fraud |
| Oranye | HIGH | Perlu investigasi, risiko tinggi |
| Kuning | MEDIUM | Cek manual, perlu klarifikasi |

---

## Catatan untuk Auditor

1. Output ini adalah **petunjuk awal** — bukan bukti konklusif.
2. Setiap temuan harus **dikonfirmasi** dengan dokumen pendukung (slip EDC, check-in card, CCTV jika perlu).
3. Temuan CRITICAL yang melibatkan **multiple reservasi + cash** memerlukan perhatian prioritas.
4. Pattern **rate change dini hari + cash tidak tercatat** (pola "Dedi") adalah red flag utama.
5. File Excel output dapat digunakan sebagai **working paper** audit.

---

## Troubleshooting

**Error "No module named 'numbers_parser'"**  
Jalankan: `pip3 install numbers-parser`

**Error "Port 5050 already in use"**  
Ubah port di `app.py` baris terakhir: `app.run(port=5051, ...)`

**File .numbers tidak terbaca**  
Pastikan file disimpan dari Apple Numbers (bukan dikonversi). Coba ekspor ke .xlsx terlebih dahulu.

**Kolom tidak dikenali**  
Pastikan format ekspor PMS sesuai dengan kolom yang diharapkan (lihat bagian Cara Ekspor di atas).
