"""FO Transaction Anomaly Checker — Split Payment & Bill Transfer Detection"""

import re
from pathlib import Path
import pandas as pd

STAR_RE = re.compile(r'^\*(\d+),\s*\d{2}/\d{2}/\d{2}\s*RmNo\s*(\d*)')

CARD_METHODS = {
    'visa', 'master', 'bni master', 'bni visa', 'bca card', 'bca amex',
    'debit card', 'debit bni', 'bca unionpay', 'bca union pay', 'bca jcb',
    'bni jcb card', 'bni amex', 'bca debit', 'bni debit', 'bca master',
    'bca visa', 'bni debit', 'payment link bca',
}

PAY_COLS = [
    'Date', 'Room Number', 'Non Stay', 'Master Bill', 'Shift', 'Bill Number',
    'Article Number', 'Description', 'Payment By', 'Voucher Number', 'Department',
    'Outlet', 'Quantity', 'Amount', 'Guest Name', 'Bill Receiver',
    'Reservation Name', 'Segment Code', 'Check-in Date', 'Check-out Date',
    'Time', 'ID', 'System Date', 'Remark', 'Nationality',
    'Reservation Number', 'Source Booking',
]


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def build_uf(edges):
    uf = UnionFind()
    for a, b in edges:
        uf.union(a, b)
    comps = {}
    for x in set(e[0] for e in edges) | set(e[1] for e in edges):
        comps.setdefault(uf.find(x), set()).add(x)
    return uf, comps


def _normalize(df):
    df = df.dropna(subset=['Bill Number']).copy()
    df['Bill Number'] = pd.to_numeric(df['Bill Number'], errors='coerce')
    df = df.dropna(subset=['Bill Number'])
    df['Bill Number'] = df['Bill Number'].astype(int)
    df['Article Number'] = pd.to_numeric(df['Article Number'], errors='coerce')
    df['DescStr'] = df['Description'].astype(str).str.strip()
    df['Room Number str'] = df['Room Number'].astype(str).str.strip()
    df['Reservation Number'] = pd.to_numeric(
        df['Reservation Number'].astype(str).str.strip(), errors='coerce')
    # Payment method: support both 'Cek' and 'Payment By' column names
    if 'Payment By' in df.columns:
        df['CekClean'] = df['Payment By'].astype(str).str.strip().str.replace(
            r'\[.*?\]', '', regex=True).str.strip()
    elif 'Cek' in df.columns:
        df['CekClean'] = df['Cek'].astype(str).str.strip().str.replace(
            r'\[.*?\]', '', regex=True).str.strip()
    else:
        df['CekClean'] = df['DescStr'].str.replace(r'\[.*?\]', '', regex=True).str.strip()
    if not pd.api.types.is_numeric_dtype(df['Amount']):
        df['Amount'] = pd.to_numeric(
            df['Amount'].astype(str).str.replace(',', '', regex=False), errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df


def load_fo_file(path):
    path = Path(path)
    ext = path.suffix.lower()

    if ext == '.numbers':
        from numbers_parser import Document
        doc = Document(str(path))
        table = doc.sheets[0].tables[0]
        data = []
        header_row = None
        for i, row in enumerate(table.iter_rows()):
            vals = [cell.value for cell in row]
            if header_row is None:
                if vals[0] == 'Date' and vals[5] == 'Bill Number':
                    header_row = vals
                continue
            data.append(vals)
        df = pd.DataFrame(data, columns=header_row if header_row else PAY_COLS[:len(data[0])])
    elif ext in ('.xlsx', '.xls'):
        df = pd.read_excel(str(path), header=None, skiprows=8, names=PAY_COLS)
    elif ext == '.csv':
        cols_no_cek = [c for c in PAY_COLS if c != 'Payment By']
        df = pd.read_csv(str(path), skiprows=7, names=cols_no_cek,
                         header=0, encoding='utf-8-sig', dtype=str)
    else:
        raise ValueError(f"Format tidak didukung: {ext}")

    return _normalize(df)


def extract_edges(df):
    edges = []
    for _, row in df[df['DescStr'].str.startswith('*')].iterrows():
        m = STAR_RE.match(row['DescStr'])
        if m:
            edges.append((int(m.group(1)), row['Bill Number']))
    return edges


def net_methods(pay_real):
    grp = pay_real.groupby(['Bill Number', 'CekClean'])['Amount'].sum().reset_index()
    return grp[grp['Amount'] != 0]


def payment_range(pay):
    return pay[(pay['Article Number'] >= 1) & (pay['Article Number'] <= 49)].copy()


def check_split_cash(pay, rev):
    payM = payment_range(pay)
    payReal = payM[~payM['DescStr'].str.startswith('*')].copy()
    grp = net_methods(payReal)
    multi = set(grp.groupby('Bill Number')['CekClean'].nunique()[lambda x: x > 1].index)
    cash_bills = set(grp[grp['CekClean'].str.contains('Cash', case=False)]['Bill Number'].unique())
    rows = []
    for b in sorted(multi & cash_bills):
        methods = grp[grp['Bill Number'] == b][['CekClean', 'Amount']].values.tolist()
        rooms = set(pay[pay['Bill Number'] == b]['Room Number str']) | \
                set(rev[rev['Bill Number'] == b]['Room Number str'])
        rooms = {r for r in rooms if r not in ('', 'nan', '*')}
        resv = set(pay[pay['Bill Number'] == b]['Reservation Number'].dropna()) | \
               set(rev[rev['Bill Number'] == b]['Reservation Number'].dropna())
        rows.append({
            'Bill Number': b,
            'Payment Methods (net)': '; '.join(f"{m} ({a:,.0f})" for m, a in methods),
            'Jumlah Metode': len(methods),
            'Room Number(s)': ', '.join(sorted(rooms)) or '(non-stay)',
            'Jumlah Kamar': len(rooms),
            'Reservation No(s)': ', '.join(str(int(x)) for x in sorted(resv)) or '-',
            'Jumlah Reservasi': len(resv),
            'ANOMALI': 'YA ⚠️' if len(rooms) > 1 and len(resv) > 1 else 'Cek manual',
            'Severity': 'CRITICAL' if len(rooms) > 1 and len(resv) > 1 else 'HIGH',
        })
    return rows


def check_bill_chain(pay, rev):
    payM = payment_range(pay)
    payReal = payM[~payM['DescStr'].str.startswith('*')].copy()
    grp = net_methods(payReal)
    edges = extract_edges(payM)
    if not edges:
        return []
    uf, comps = build_uf(edges)
    rows = []
    for root, members in comps.items():
        if len(members) <= 1:
            continue
        members = sorted(members)
        sub = grp[grp['Bill Number'].isin(members)]
        methods = sub.groupby('CekClean')['Amount'].sum()
        methods = methods[methods != 0]
        has_cash = methods.index.str.contains('Cash', case=False).any()
        rooms = set()
        resv = set()
        for b in members:
            rooms |= {r for r in pay[pay['Bill Number'] == b]['Room Number str']
                      if r not in ('', 'nan', '*')}
            rooms |= {r for r in rev[rev['Bill Number'] == b]['Room Number str']
                      if r not in ('', 'nan', '*')}
            resv |= set(pay[pay['Bill Number'] == b]['Reservation Number'].dropna())
            resv |= set(rev[rev['Bill Number'] == b]['Reservation Number'].dropna())
        if len(methods) > 1 and has_cash and len(rooms) > 1 and len(resv) > 1:
            status = 'CRITICAL — SPLIT PAYMENT ANOMALI'
        elif has_cash and len(rooms) > 1 and len(resv) > 1:
            status = 'HIGH — CASH TRANSFER ANTAR FOLIO'
        else:
            continue
        rows.append({
            'Bill Chain': ', '.join(str(m) for m in members),
            'Jumlah Bill': len(members),
            'Payment Methods (net)': '; '.join(f"{m} ({a:,.0f})" for m, a in methods.items()),
            'Jumlah Metode': len(methods),
            'Ada Cash?': 'Ya' if has_cash else 'Tidak',
            'Room Number(s)': ', '.join(sorted(rooms)) or '-',
            'Jumlah Kamar': len(rooms),
            'Reservation No(s)': ', '.join(str(int(x)) for x in sorted(resv)) or '-',
            'Jumlah Reservasi': len(resv),
            'Status': status,
            'Severity': 'CRITICAL' if 'CRITICAL' in status else 'HIGH',
        })
    return sorted(rows, key=lambda x: -x['Jumlah Kamar'])


def check_room_consolidation(pay, rev):
    charges = rev[rev['Article Number'] == 99]
    real_room = charges[~charges['DescStr'].str.startswith('*')].drop_duplicates(
        'Bill Number').set_index('Bill Number')['Room Number str'].to_dict()
    real_resv = charges[~charges['DescStr'].str.startswith('*')].drop_duplicates(
        'Bill Number').set_index('Bill Number')['Reservation Number'].to_dict()

    star_rows = charges[charges['DescStr'].str.startswith('*')].copy()
    edges_data = []
    for _, row in star_rows.iterrows():
        m = STAR_RE.match(row['DescStr'])
        if m:
            edges_data.append((row['Bill Number'], int(m.group(1)), m.group(2).strip()))

    if not edges_data:
        return []

    pay_edges = extract_edges(payment_range(pay))
    rev_edges = extract_edges(rev)
    uf_all, comps_all = build_uf(pay_edges + rev_edges)

    payReal = payment_range(pay)[~payment_range(pay)['DescStr'].str.startswith('*')].copy()

    rows_out = []
    seen_keys = set()
    for dest_bill, src_bill, src_room_text in edges_data:
        rooms = {real_room.get(src_bill) or src_room_text}
        resv = set()
        if real_resv.get(src_bill):
            resv.add(real_resv[src_bill])
        own_room = real_room.get(dest_bill)
        own_resv = real_resv.get(dest_bill)
        if own_room:
            rooms.add(own_room)
        if own_resv and pd.notna(own_resv):
            resv.add(own_resv)
        rooms = {r for r in rooms if r and str(r).strip()}
        if len(rooms) <= 1:
            continue
        comp = comps_all.get(uf_all.find(dest_bill), {dest_bill}) \
            if dest_bill in uf_all.parent else {dest_bill}
        pay_rows = payReal[payReal['Bill Number'].isin(comp)]
        methods = pay_rows.groupby('CekClean')['Amount'].sum()
        methods = methods[methods != 0]
        is_card_cash = (
            len(methods) == 2 and
            any('cash' in k.lower() for k in methods.index) and
            any(k.lower() in CARD_METHODS for k in methods.index)
        )
        if not is_card_cash or len(resv) <= 1:
            continue
        key = str(sorted(comp & set(payReal['Bill Number'].unique())))
        if key in seen_keys:
            continue
        seen_keys.add(key)
        rows_out.append({
            'Dest Bill': dest_bill,
            'Semua Kamar Tergabung': ', '.join(sorted(str(r) for r in rooms)),
            'Jumlah Kamar': len(rooms),
            'Reservasi Tergabung': ', '.join(str(int(r)) for r in sorted(resv) if pd.notna(r)),
            'Jumlah Reservasi': len(resv),
            'Payment Bills': ', '.join(str(v) for v in sorted(comp & set(payReal['Bill Number'].unique()))),
            'Metode Pembayaran': '; '.join(f"{k} ({v:,.0f})" for k, v in methods.items()),
            'Severity': 'CRITICAL',
            'Keterangan': 'Room charge lintas kamar dibayar Card+Cash — anomali kuat',
        })
    return rows_out


def check_room_no_payment(pay, rev, period_end=None):
    payM = payment_range(pay)
    payReal = payM[~payM['DescStr'].str.startswith('*')].copy()
    real_rc = set(rev[(rev['Article Number'] == 99) & (~rev['DescStr'].str.startswith('*'))]['Bill Number'].unique())
    paid = set(payReal['Bill Number'].unique())

    pay_edges = extract_edges(payM)
    rev_edges = extract_edges(rev)
    uf_all, comps_all = build_uf(pay_edges + rev_edges)

    no_pay = []
    for b in sorted(real_rc):
        if b in paid:
            continue
        if b in uf_all.parent:
            comp = comps_all[uf_all.find(b)]
            if comp & paid:
                continue
        no_pay.append(b)

    sub = rev[(rev['Bill Number'].isin(no_pay)) & (rev['Article Number'] == 99) &
              (~rev['DescStr'].str.startswith('*'))]
    agg = sub.groupby('Bill Number').agg(
        Room=('Room Number str', 'first'), CheckIn=('Check-in Date', 'first'),
        CheckOut=('Check-out Date', 'first'), Total=('Amount', 'sum'),
        Guest=('Guest Name', 'first'), BillReceiver=('Bill Receiver', 'first'),
    ).reset_index()

    rows = []
    for _, r in agg.iterrows():
        br = str(r['BillReceiver']).strip()
        if br in ('[INDIVIDUAL RESERVATION]', '[WALK IN GUEST],', 'nan', ''):
            kategori = 'PERLU DICEK — Tamu individual/walk-in checkout tanpa pembayaran'
            sev = 'CRITICAL'
        else:
            kategori = 'OTA/Korporat — kemungkinan city ledger'
            sev = 'MEDIUM'
        rows.append({
            'Bill Number': r['Bill Number'], 'Room': r['Room'],
            'Check-in': r['CheckIn'], 'Check-out': r['CheckOut'],
            'Total Room Charge': r['Total'], 'Guest': r['Guest'],
            'Bill Receiver': br, 'Kategori': kategori,
            'Severity': sev,
        })
    return sorted(rows, key=lambda x: x['Severity'])
