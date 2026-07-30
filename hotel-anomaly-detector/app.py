"""
Hotel FO Anomaly Detector — Web App
Jalankan: python app.py
Buka: http://localhost:5050
"""

import os
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime

from flask import Flask, request, jsonify, send_file, render_template_string
import openpyxl

sys.path.insert(0, str(Path(__file__).parent))
from analyzers import rate_change, fo_anomaly, excel_writer

UPLOAD_DIR = Path(__file__).parent / 'uploads'
OUTPUT_DIR = Path(__file__).parent / 'outputs'
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# ── HTML UI ──────────────────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hotel FO Anomaly Detector</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, sans-serif; background: #f0f2f5; color: #1a1a2e; }
  .header { background: #2E4057; color: white; padding: 20px 32px; }
  .header h1 { font-size: 22px; }
  .header p { font-size: 13px; opacity: 0.8; margin-top: 4px; }
  .container { max-width: 960px; margin: 32px auto; padding: 0 20px; }
  .card { background: white; border-radius: 10px; padding: 28px; margin-bottom: 24px;
          box-shadow: 0 2px 8px rgba(0,0,0,.08); }
  .card h2 { font-size: 16px; color: #2E4057; margin-bottom: 18px;
             border-bottom: 2px solid #e8ecf0; padding-bottom: 10px; }
  .tab-bar { display: flex; gap: 8px; margin-bottom: 24px; }
  .tab { padding: 10px 22px; border-radius: 6px; cursor: pointer; font-size: 14px;
         border: 2px solid #dee2e6; background: white; color: #666; transition: all .2s; }
  .tab.active { background: #2E4057; color: white; border-color: #2E4057; }
  .tab:hover:not(.active) { border-color: #2E4057; color: #2E4057; }
  .panel { display: none; } .panel.active { display: block; }
  .upload-zone { border: 2px dashed #b0bec5; border-radius: 8px; padding: 32px;
                 text-align: center; cursor: pointer; transition: all .2s; background: #f8f9fa; }
  .upload-zone:hover, .upload-zone.drag { border-color: #2E4057; background: #eef2f7; }
  .upload-zone input { display: none; }
  .upload-zone .icon { font-size: 36px; margin-bottom: 10px; }
  .upload-zone p { color: #666; font-size: 14px; }
  .upload-zone .hint { font-size: 12px; color: #999; margin-top: 6px; }
  .file-list { margin-top: 12px; }
  .file-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px;
               background: #f8f9fa; border-radius: 6px; margin-top: 6px; font-size: 13px; }
  .file-item .name { flex: 1; }
  .file-item .remove { color: #e53e3e; cursor: pointer; font-size: 16px; }
  .btn { display: inline-block; padding: 12px 28px; border-radius: 8px; font-size: 15px;
         font-weight: bold; cursor: pointer; border: none; transition: all .2s; }
  .btn-primary { background: #2E4057; color: white; width: 100%; text-align: center;
                 margin-top: 18px; }
  .btn-primary:hover { background: #3d5a80; }
  .btn-primary:disabled { background: #aaa; cursor: not-allowed; }
  .btn-download { background: #38a169; color: white; padding: 10px 22px; font-size: 14px; }
  .btn-download:hover { background: #2f855a; }
  .progress { display: none; margin-top: 16px; }
  .progress-bar { height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }
  .progress-fill { height: 100%; background: #2E4057; width: 0%; transition: width .3s;
                   border-radius: 4px; }
  .progress-text { font-size: 13px; color: #666; margin-top: 6px; }
  .results { display: none; margin-top: 20px; }
  .result-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                 gap: 14px; margin-bottom: 20px; }
  .result-card { border-radius: 8px; padding: 16px; text-align: center; }
  .result-card.critical { background: #fff5f5; border: 1px solid #fed7d7; }
  .result-card.high { background: #fffaf0; border: 1px solid #feebc8; }
  .result-card.medium { background: #fffff0; border: 1px solid #fefcbf; }
  .result-card.ok { background: #f0fff4; border: 1px solid #c6f6d5; }
  .result-card .count { font-size: 32px; font-weight: bold; }
  .result-card.critical .count { color: #e53e3e; }
  .result-card.high .count { color: #dd6b20; }
  .result-card.medium .count { color: #d69e2e; }
  .result-card.ok .count { color: #38a169; }
  .result-card .label { font-size: 12px; color: #666; margin-top: 4px; }
  .alert { padding: 12px 16px; border-radius: 6px; font-size: 13px; margin-top: 10px; }
  .alert-error { background: #fff5f5; border: 1px solid #fed7d7; color: #c53030; }
  .alert-success { background: #f0fff4; border: 1px solid #c6f6d5; color: #276749; }
  .section-title { font-size: 13px; font-weight: bold; color: #2E4057;
                   margin: 16px 0 8px 0; }
  label { font-size: 13px; color: #444; display: block; margin-bottom: 4px; }
  select, input[type=text] { width: 100%; padding: 8px 12px; border: 1px solid #dee2e6;
    border-radius: 6px; font-size: 13px; margin-bottom: 12px; }
</style>
</head>
<body>

<div class="header">
  <h1>🏨 Hotel FO Anomaly Detector</h1>
  <p>Deteksi anomali Front Office: Rate Change · Split Payment · Bill Transfer · Room Consolidation</p>
</div>

<div class="container">

  <div class="tab-bar">
    <div class="tab active" onclick="switchTab('rate')">📊 Rate Change</div>
    <div class="tab" onclick="switchTab('fo')">💳 FO Transaction</div>
  </div>

  <!-- RATE CHANGE PANEL -->
  <div id="panel-rate" class="panel active">
    <div class="card">
      <h2>Rate Change Anomaly Detector</h2>
      <p style="font-size:13px;color:#666;margin-bottom:18px">
        Upload <strong>Change Room Rate Report</strong> dari PMS (.numbers / .xlsx / .csv)
      </p>
      <label>Label Properti</label>
      <input type="text" id="rate-label" placeholder="contoh: Yello Hotel Kuta Beachwalk — Mei 2026">
      <div class="upload-zone" id="rate-zone" onclick="document.getElementById('rate-file').click()"
           ondragover="event.preventDefault();this.classList.add('drag')"
           ondragleave="this.classList.remove('drag')"
           ondrop="handleDrop(event,'rate-file','rate-zone')">
        <input type="file" id="rate-file" accept=".numbers,.xlsx,.xls,.csv"
               onchange="showFile(this,'rate-files')">
        <div class="icon">📁</div>
        <p>Klik atau drag file ke sini</p>
        <p class="hint">Format: .numbers · .xlsx · .csv</p>
      </div>
      <div class="file-list" id="rate-files"></div>
      <button class="btn btn-primary" id="rate-btn" onclick="runRateChange()" disabled>
        🔍 ANALISIS RATE CHANGE
      </button>
      <div class="progress" id="rate-progress">
        <div class="progress-bar"><div class="progress-fill" id="rate-fill"></div></div>
        <div class="progress-text" id="rate-text">Memproses...</div>
      </div>
      <div class="results" id="rate-results"></div>
    </div>
  </div>

  <!-- FO TRANSACTION PANEL -->
  <div id="panel-fo" class="panel">
    <div class="card">
      <h2>FO Transaction Anomaly Checker</h2>
      <p style="font-size:13px;color:#666;margin-bottom:18px">
        Upload <strong>FO Transaction Journal</strong> Payment (Article 1-49) &
        Revenue (Article 99-100)
      </p>
      <label>Label Properti</label>
      <input type="text" id="fo-label" placeholder="contoh: Yello Hotel Kuta Beachwalk — April 2026">
      <div class="section-title">File Payment (Article 1–49)</div>
      <div class="upload-zone" id="fo-pay-zone" onclick="document.getElementById('fo-pay').click()"
           ondragover="event.preventDefault();this.classList.add('drag')"
           ondragleave="this.classList.remove('drag')"
           ondrop="handleDrop(event,'fo-pay','fo-pay-zone')">
        <input type="file" id="fo-pay" accept=".numbers,.xlsx,.xls,.csv"
               onchange="showFile(this,'fo-pay-files')">
        <div class="icon">💳</div>
        <p>File Payment</p>
        <p class="hint">Format: .numbers · .xlsx · .csv</p>
      </div>
      <div class="file-list" id="fo-pay-files"></div>
      <div class="section-title" style="margin-top:18px">File Revenue Room (Article 99–100)</div>
      <div class="upload-zone" id="fo-rev-zone" onclick="document.getElementById('fo-rev').click()"
           ondragover="event.preventDefault();this.classList.add('drag')"
           ondragleave="this.classList.remove('drag')"
           ondrop="handleDrop(event,'fo-rev','fo-rev-zone')">
        <input type="file" id="fo-rev" accept=".numbers,.xlsx,.xls,.csv"
               onchange="showFile(this,'fo-rev-files')">
        <div class="icon">🏨</div>
        <p>File Revenue Room</p>
        <p class="hint">Format: .numbers · .xlsx · .csv</p>
      </div>
      <div class="file-list" id="fo-rev-files"></div>
      <button class="btn btn-primary" id="fo-btn" onclick="runFO()" disabled>
        🔍 ANALISIS FO TRANSACTION
      </button>
      <div class="progress" id="fo-progress">
        <div class="progress-bar"><div class="progress-fill" id="fo-fill"></div></div>
        <div class="progress-text" id="fo-text">Memproses...</div>
      </div>
      <div class="results" id="fo-results"></div>
    </div>
  </div>

</div>

<script>
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  event.target.classList.add('active');
}

function showFile(input, listId) {
  const list = document.getElementById(listId);
  if (!input.files.length) return;
  list.innerHTML = '';
  Array.from(input.files).forEach(f => {
    list.innerHTML += `<div class="file-item">
      <span>📄</span><span class="name">${f.name} (${(f.size/1024).toFixed(0)} KB)</span>
    </div>`;
  });
  checkButtons();
}

function handleDrop(event, inputId, zoneId) {
  event.preventDefault();
  document.getElementById(zoneId).classList.remove('drag');
  const dt = event.dataTransfer;
  const input = document.getElementById(inputId);
  input.files = dt.files;
  showFile(input, inputId.replace('-', '-') + '-files');
}

function checkButtons() {
  document.getElementById('rate-btn').disabled = !document.getElementById('rate-file').files.length;
  const payOk = document.getElementById('fo-pay').files.length;
  const revOk = document.getElementById('fo-rev').files.length;
  document.getElementById('fo-btn').disabled = !(payOk && revOk);
}

function setProgress(prefix, pct, text) {
  document.getElementById(prefix + '-progress').style.display = 'block';
  document.getElementById(prefix + '-fill').style.width = pct + '%';
  document.getElementById(prefix + '-text').textContent = text;
}

function showResultCards(prefix, sheets) {
  const el = document.getElementById(prefix + '-results');
  el.style.display = 'block';
  const cards = sheets.map(s => {
    const cls = s.count > 0 ? (s.severity || 'high') : 'ok';
    return `<div class="result-card ${cls}">
      <div class="count">${s.count}</div>
      <div class="label">${s.label}</div>
    </div>`;
  }).join('');
  el.innerHTML = `<div class="result-grid">${cards}</div>
    <button class="btn btn-download" onclick="downloadFile('${prefix}')">
      ⬇️ Download Excel Report
    </button>
    <div id="${prefix}-msg"></div>`;
}

async function runRateChange() {
  const file = document.getElementById('rate-file').files[0];
  const label = document.getElementById('rate-label').value || 'Hotel';
  if (!file) return;
  document.getElementById('rate-btn').disabled = true;
  setProgress('rate', 20, 'Membaca file...');
  const fd = new FormData();
  fd.append('file', file);
  fd.append('label', label);
  try {
    setProgress('rate', 50, 'Mendeteksi anomali rate change...');
    const res = await fetch('/api/rate-change', { method: 'POST', body: fd });
    const data = await res.json();
    setProgress('rate', 100, 'Selesai!');
    if (data.error) {
      document.getElementById('rate-results').style.display = 'block';
      document.getElementById('rate-results').innerHTML =
        `<div class="alert alert-error">❌ Error: ${data.error}</div>`;
    } else {
      showResultCards('rate', [
        { label: 'Rate Turun >30%', count: data.s1, severity: data.s1 > 0 ? 'critical' : 'ok' },
        { label: 'Rate Hampir Nol', count: data.s2, severity: data.s2 > 0 ? 'critical' : 'ok' },
        { label: 'Perubahan Dini Hari', count: data.s3, severity: data.s3 > 0 ? 'critical' : 'ok' },
        { label: 'Tanpa Staff ID', count: data.s4, severity: data.s4 > 0 ? 'high' : 'ok' },
        { label: 'Multiple Changes', count: data.s5, severity: data.s5 > 0 ? 'high' : 'ok' },
      ]);
      window._rateFile = data.filename;
    }
  } catch(e) {
    setProgress('rate', 0, '');
    alert('Error: ' + e.message);
  }
  document.getElementById('rate-btn').disabled = false;
}

async function runFO() {
  const pay = document.getElementById('fo-pay').files[0];
  const rev = document.getElementById('fo-rev').files[0];
  const label = document.getElementById('fo-label').value || 'Hotel';
  if (!pay || !rev) return;
  document.getElementById('fo-btn').disabled = true;
  setProgress('fo', 20, 'Membaca file payment...');
  const fd = new FormData();
  fd.append('pay_file', pay);
  fd.append('rev_file', rev);
  fd.append('label', label);
  try {
    setProgress('fo', 50, 'Mendeteksi anomali transaksi FO...');
    const res = await fetch('/api/fo-anomaly', { method: 'POST', body: fd });
    const data = await res.json();
    setProgress('fo', 100, 'Selesai!');
    if (data.error) {
      document.getElementById('fo-results').style.display = 'block';
      document.getElementById('fo-results').innerHTML =
        `<div class="alert alert-error">❌ Error: ${data.error}</div>`;
    } else {
      showResultCards('fo', [
        { label: 'Split Payment + Cash', count: data.s1, severity: data.s1 > 0 ? 'critical' : 'ok' },
        { label: 'Bill Transfer Chain', count: data.s2, severity: data.s2 > 0 ? 'critical' : 'ok' },
        { label: 'Room Consolidation Card+Cash', count: data.s3, severity: data.s3 > 0 ? 'critical' : 'ok' },
        { label: 'Room Tanpa Pembayaran', count: data.s4, severity: data.s4 > 0 ? 'high' : 'ok' },
      ]);
      window._foFile = data.filename;
    }
  } catch(e) {
    setProgress('fo', 0, '');
    alert('Error: ' + e.message);
  }
  document.getElementById('fo-btn').disabled = false;
}

async function downloadFile(prefix) {
  const filename = prefix === 'rate' ? window._rateFile : window._foFile;
  if (!filename) return;
  const a = document.createElement('a');
  a.href = '/download/' + filename;
  a.download = filename;
  a.click();
}

document.querySelectorAll('input[type=file]').forEach(i => {
  i.addEventListener('change', checkButtons);
});
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/acl')
def acl():
    acl_path = Path(__file__).parent / 'ACL_INPP.html'
    if acl_path.exists():
        return acl_path.read_text(encoding='utf-8')
    return "File ACL_INPP.html tidak ditemukan.", 404


@app.route('/api/rate-change', methods=['POST'])
def api_rate_change():
    try:
        f = request.files.get('file')
        label = request.form.get('label', 'Hotel')
        if not f:
            return jsonify({'error': 'File tidak ditemukan'})

        path = UPLOAD_DIR / f.filename
        f.save(str(path))

        rows = rate_change.load_file(str(path))
        s1, s2, s3, s4, s5 = rate_change.analyze(rows)

        wb = openpyxl.Workbook()
        wb.remove(wb.active)

        sheets_info = [
            (1, '1. Rate Turun >30%', 'Rate kamar turun >30%', len(s1), 'CRITICAL', 'Segera'),
            (2, '2. Rate Hampir Nol', 'Rate turun ke < Rp 10.000', len(s2), 'CRITICAL', 'Segera'),
            (3, '3. Perubahan Dini Hari', 'Rate diubah pukul 22:00-06:00', len(s3), 'CRITICAL', 'Segera'),
            (4, '4. Tanpa Staff ID', 'Rate berubah tanpa ID staff', len(s4), 'HIGH', '1 minggu'),
            (5, '5. Multiple Changes', '>1x perubahan per reservasi/hari', len(s5), 'HIGH', '1 minggu'),
        ]
        excel_writer.write_summary(wb, label, sheets_info)

        excel_writer.write_sheet(wb, '1. Rate Turun >30%',
            ['Reservation No','Room No','Guest Name','Status','Arrival','Departure',
             'Rate Lama','Rate Baru','Selisih','Penurunan %','Staff ID (ubah)',
             'Staff ID (approve)','Change Date','Change Time','Dini Hari?','Severity','Keterangan'],
            s1, [12,8,28,14,12,12,14,14,14,12,14,16,14,12,12,12,40])

        excel_writer.write_sheet(wb, '2. Rate Hampir Nol',
            ['Reservation No','Room No','Guest Name','Status','Rate Lama','Rate Baru',
             'Selisih','Staff ID','Change Date','Change Time','Severity','Keterangan'],
            s2, [12,8,28,14,14,14,14,14,14,12,12,40])

        excel_writer.write_sheet(wb, '3. Perubahan Dini Hari',
            ['Reservation No','Room No','Guest Name','Status','Rate Lama','Rate Baru',
             'Selisih','Arah','Staff ID','Change Date','Change Time','Severity','Keterangan'],
            s3, [12,8,28,14,14,14,14,12,14,14,12,12,40])

        excel_writer.write_sheet(wb, '4. Tanpa Staff ID',
            ['Reservation No','Room No','Guest Name','Status','Rate Lama','Rate Baru',
             'Selisih','Change Date','Change Time','Severity','Keterangan'],
            s4, [12,8,28,14,14,14,14,14,12,12,40])

        excel_writer.write_sheet(wb, '5. Multiple Changes',
            ['Reservation No','Change Date','Room No','Guest Name','Status',
             'Jumlah Perubahan','Kronologi Rate','Staff IDs','Times','Severity','Keterangan'],
            s5, [12,14,8,28,14,14,60,22,22,12,40])

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_name = f"RateChange_Anomaly_{ts}.xlsx"
        wb.save(str(OUTPUT_DIR / out_name))

        return jsonify({'s1': len(s1), 's2': len(s2), 's3': len(s3),
                        's4': len(s4), 's5': len(s5), 'filename': out_name})

    except Exception as e:
        return jsonify({'error': str(e) + '\n' + traceback.format_exc()})


@app.route('/api/fo-anomaly', methods=['POST'])
def api_fo_anomaly():
    try:
        pay_file = request.files.get('pay_file')
        rev_file = request.files.get('rev_file')
        label = request.form.get('label', 'Hotel')
        if not pay_file or not rev_file:
            return jsonify({'error': 'File payment atau revenue tidak ditemukan'})

        pay_path = UPLOAD_DIR / pay_file.filename
        rev_path = UPLOAD_DIR / rev_file.filename
        pay_file.save(str(pay_path))
        rev_file.save(str(rev_path))

        pay = fo_anomaly.load_fo_file(str(pay_path))
        rev = fo_anomaly.load_fo_file(str(rev_path))

        s1 = fo_anomaly.check_split_cash(pay, rev)
        s2 = fo_anomaly.check_bill_chain(pay, rev)
        s3 = fo_anomaly.check_room_consolidation(pay, rev)
        s4 = fo_anomaly.check_room_no_payment(pay, rev)

        wb = openpyxl.Workbook()
        wb.remove(wb.active)

        sheets_info = [
            (1, '1. Split Payment + Cash', 'Split payment ada cash lintas kamar', len(s1), 'CRITICAL', 'Segera'),
            (2, '2. Bill Transfer Chain', 'Rantai bill terhubung via transfer', len(s2), 'CRITICAL', 'Segera'),
            (3, '3. Room Consolidation Card+Cash', 'Room charge digabung, bayar Card+Cash', len(s3), 'CRITICAL', 'Segera'),
            (4, '4. Room Tanpa Pembayaran', 'Room charge ada tapi tidak ada pembayaran', len(s4), 'HIGH', '1 minggu'),
        ]
        excel_writer.write_summary(wb, label, sheets_info)

        excel_writer.write_sheet(wb, '1. Split Payment + Cash',
            ['Bill Number','Payment Methods (net)','Jumlah Metode','Room Number(s)',
             'Jumlah Kamar','Reservation No(s)','Jumlah Reservasi','ANOMALI','Severity'],
            s1, [12, 55, 12, 22, 12, 22, 14, 28, 12])

        excel_writer.write_sheet(wb, '2. Bill Transfer Chain',
            ['Bill Chain','Jumlah Bill','Payment Methods (net)','Jumlah Metode',
             'Ada Cash?','Room Number(s)','Jumlah Kamar','Reservation No(s)',
             'Jumlah Reservasi','Status','Severity'],
            s2, [25, 10, 55, 12, 10, 22, 12, 22, 14, 45, 12])

        excel_writer.write_sheet(wb, '3. Room Consolidation Card+Cash',
            ['Dest Bill','Semua Kamar Tergabung','Jumlah Kamar','Reservasi Tergabung',
             'Jumlah Reservasi','Payment Bills','Metode Pembayaran','Severity','Keterangan'],
            s3, [12, 28, 12, 28, 14, 22, 45, 12, 45])

        excel_writer.write_sheet(wb, '4. Room Tanpa Pembayaran',
            ['Bill Number','Room','Check-in','Check-out','Total Room Charge',
             'Guest','Bill Receiver','Kategori','Severity'],
            s4, [12, 8, 14, 14, 18, 28, 28, 45, 12])

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_name = f"FO_Anomaly_{ts}.xlsx"
        wb.save(str(OUTPUT_DIR / out_name))

        return jsonify({'s1': len(s1), 's2': len(s2), 's3': len(s3),
                        's4': len(s4), 'filename': out_name})

    except Exception as e:
        return jsonify({'error': str(e) + '\n' + traceback.format_exc()})


@app.route('/download/<filename>')
def download(filename):
    path = OUTPUT_DIR / filename
    if not path.exists():
        return 'File tidak ditemukan', 404
    return send_file(str(path), as_attachment=True, download_name=filename)


if __name__ == '__main__':
    print("=" * 55)
    print("  Hotel FO Anomaly Detector")
    print("  Buka browser: http://localhost:5050")
    print("=" * 55)
    app.run(host='0.0.0.0', port=5050, debug=False)
