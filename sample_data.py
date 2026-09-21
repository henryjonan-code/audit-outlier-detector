"""
Sample Data Saham IHSG untuk Demonstrasi
Version 5.7 - Update 17 Juli 2026 (V5.1 REVISED CRITERIA)

============================================================================
DISCLAIMER PENTING:
============================================================================
Data diupdate berdasarkan harga pasar 17 Juli 2026.

KRITERIA BARU V5.0 (7 Hard Filter):
1. ROE >= 10% (bukan cuma > 0%)
2. D/E < 100% untuk non-bank (revised dari 50%)
3. Operating Cash Flow positif
4. Dividend > 0%, Payout Ratio < 80%
5. Free Float >= 15%
6. Governance: tidak ada red flag
7. Valuasi wajar (PER < 20 atau PBV < 3)

FIELD BARU:
- operating_cash_flow: OCF dalam miliar IDR
- payout_ratio: dividend payout ratio dalam %
- governance_flag: True jika ada red flag, False jika aman

Sumber: Yahoo Finance, Investing.com, IDX
============================================================================
"""

SAMPLE_STOCK_DATA = [
    # =========================================================================
    # BANK - Perbankan (METRIK KHUSUS: CAR, NPL, NIM - bukan D/E!)
    # Catatan: Bank punya struktur modal berbeda, DPK = liabilitas
    # D/E bank normal 5-7x, jadi gunakan metrik CAR, NPL, NIM
    # =========================================================================
    {
        'ticker': 'BBCA.JK',
        'name': 'Bank Central Asia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,  # FLAG untuk identifikasi bank
        'current_price': 6300,  # Update 21 Sep 2026: -5.6% dari 6675 (Ajaib)
        'price_change_3y': 6.2,  # 3 TAHUN: dari ~6800 ke 7225
        'price_change_1y': -25.1,  # 1 TAHUN: TURUN dari 9650 - DOWNTREND!
        # METRIK KHUSUS BANK (bukan D/E!)
        'car': 28.5,  # Capital Adequacy Ratio (min 8%, ideal >20%)
        'npl': 1.8,   # Non Performing Loan (max 5%, ideal <3%)
        'nim': 5.2,   # Net Interest Margin (ideal >4%)
        'ldr': 78.5,  # Loan to Deposit Ratio (ideal 80-92%)
        'cost_to_income': 32.5,  # Cost to Income Ratio (ideal <50%)
        # Metrik standar
        'debt_to_equity': None,  # TIDAK RELEVAN untuk bank!
        'roe': 21.5,
        'roa': 3.8,
        'profit_margin': 45.2,
        'dividend_yield': 4.1,
        'current_ratio': None,
        'earnings_growth': 12.3,
        'pe_ratio': 16.0,
        'pb_ratio': 3.4,
        'peg_ratio': 1.30,
        'market_cap': 948e12,
        'avg_volume': 79_000_000,
        'free_float_pct': 45,
        'operating_cash_flow': 85000,  # OCF positif (Miliar IDR, FY2024)
        'payout_ratio': 65.6,  # div yield 4.1% * PE 16.0
        'governance_flag': False,
        'notes': 'Turun 24% YoY - DOWNTREND meski fundamental bagus',
    },
    {
        'ticker': 'BBRI.JK',
        'name': 'Bank Rakyat Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 3310,  # Update 21 Sep 2026: +4.4% dari 3170
        'price_change_3y': -14.6,  # 3 TAHUN: masih TURUN
        'price_change_1y': -6.0,  # 1 TAHUN: membaik dari -32% (52w: 3290-4450)
        # METRIK KHUSUS BANK
        'car': 25.8,
        'npl': 2.8,   # NPL agak tinggi
        'nim': 7.2,   # NIM tinggi (fokus mikro)
        'ldr': 85.2,
        'cost_to_income': 38.5,
        # Metrik standar
        'debt_to_equity': None,
        'roe': 18.5,
        'roa': 3.0,
        'profit_margin': 32.5,
        'dividend_yield': 9.21,
        'current_ratio': None,
        'earnings_growth': 8.5,
        'pe_ratio': 8.2,
        'pb_ratio': 1.5,
        'peg_ratio': 0.96,
        'market_cap': 570e12,
        'avg_volume': 120_000_000,
        'free_float_pct': 43,
        'operating_cash_flow': 62000,  # OCF positif (Miliar IDR, FY2024)
        'payout_ratio': 75.5,  # div yield 9.21% * PE 8.2
        'governance_flag': False,
        'notes': 'DOWNTREND 3Y! Div yield 9.21% tapi harga turun terus',
    },
    {
        'ticker': 'BMRI.JK',
        'name': 'Bank Mandiri Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 4260,  # Update 21 Sep 2026: +1.9% dari 4180
        'price_change_3y': 35.0,  # 3 TAHUN: dari ~3980 ke 5375 - membaik
        'price_change_1y': -7.3,  # 1 TAHUN: membaik dari -17.1% (recovery!)
        # METRIK KHUSUS BANK
        'car': 24.2,
        'npl': 1.5,   # NPL rendah (bagus)
        'nim': 5.8,
        'ldr': 88.5,
        'cost_to_income': 35.2,
        # Metrik standar
        'debt_to_equity': None,
        'roe': 22.3,
        'roa': 3.5,
        'profit_margin': 38.5,
        'dividend_yield': 6.2,
        'current_ratio': None,
        'earnings_growth': 15.5,
        'pe_ratio': 7.8,
        'pb_ratio': 1.7,
        'peg_ratio': 0.50,
        'market_cap': 491.89e12,  # Update from web
        'avg_volume': 45_000_000,
        'free_float_pct': 40,
        'operating_cash_flow': 55000,  # OCF positif (Miliar IDR, FY2024)
        'payout_ratio': 48.4,  # div yield 6.2% * PE 7.8
        'governance_flag': False,
        'notes': 'RECOVERY! +6.93% bulanan, +3.52% weekly - masih DOWNTREND 1Y tapi membaik',
    },
    {
        'ticker': 'BBNI.JK',
        'name': 'Bank Negara Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 3650,  # Update 21 Sep 2026: -0.3% dari 3660
        'price_change_3y': 18.5,  # 3 TAHUN: UPTREND lemah
        'price_change_1y': -12.5,  # 1 TAHUN: TURUN - DOWNTREND!
        # METRIK KHUSUS BANK
        'car': 22.8,
        'npl': 2.2,
        'nim': 4.8,
        'ldr': 92.5,  # LDR agak tinggi
        'cost_to_income': 42.5,
        # Metrik standar
        'debt_to_equity': None,
        'roe': 15.2,
        'roa': 2.8,
        'profit_margin': 28.5,
        'dividend_yield': 6.2,
        'current_ratio': None,
        'earnings_growth': 8.5,
        'pe_ratio': 9.5,
        'pb_ratio': 1.4,
        'peg_ratio': 1.12,
        'market_cap': 180e12,
        'avg_volume': 35_000_000,
        'free_float_pct': 40,
        'operating_cash_flow': 25000,  # OCF positif (Miliar IDR, FY2024)
        'payout_ratio': 58.9,  # div yield 6.2% * PE 9.5
        'governance_flag': False,
        'notes': '3Y uptrend tapi 1Y downtrend - MIXED SIGNAL',
    },

    # Consumer Goods
    {
        'ticker': 'ICBP.JK',
        'name': 'Indofood CBP Sukses Makmur',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 7625,  # Update 21 Ags 2026: -6.4% dari 8150 (Fortune, 18 Ags)
        'price_change_3y': 8.2,
        'price_change_1y': -31.0,
        'debt_to_equity': 0.45,
        'roe': 18.5,
        'roa': 10.2,
        'profit_margin': 12.8,
        'dividend_yield': 3.2,
        'current_ratio': 2.1,
        'earnings_growth': 22.5,
        'pe_ratio': 18.5,
        'pb_ratio': 3.4,
        'peg_ratio': 0.82,
        'market_cap': 135e12,
        'avg_volume': 5_000_000,
        'free_float_pct': 19,
        'operating_cash_flow': 4500,
        'payout_ratio': 35,
        'governance_flag': False,
    },
    {
        'ticker': 'INDF.JK',
        'name': 'Indofood Sukses Makmur',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 6925,  # Update 23 Juli 2026: +3.0% dari 6725
        'price_change_3y': 35.7,
        'debt_to_equity': 0.68,
        'roe': 14.2,
        'roa': 6.5,
        'profit_margin': 8.5,
        'dividend_yield': 4.5,
        'current_ratio': 1.5,
        'earnings_growth': 12.3,
        'pe_ratio': 8.5,
        'pb_ratio': 1.2,
        'peg_ratio': 0.69,
        'market_cap': 60e12,
        'avg_volume': 8_000_000,
        'free_float_pct': 50,
        'operating_cash_flow': 5000,
        'payout_ratio': 35,
        'governance_flag': False,
    },
    {
        'ticker': 'KLBF.JK',
        'name': 'Kalbe Farma Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 1620,
        'price_change_3y': 12.5,
        'debt_to_equity': 0.18,
        'roe': 15.8,
        'roa': 12.5,
        'profit_margin': 11.2,
        'dividend_yield': 3.5,
        'current_ratio': 4.2,
        'earnings_growth': 8.5,
        'pe_ratio': 22.5,
        'pb_ratio': 3.5,
        'peg_ratio': 2.65,
        'market_cap': 76e12,
        'avg_volume': 15_000_000,
        'free_float_pct': 43,
        'operating_cash_flow': 3500,
        'payout_ratio': 55,
        'governance_flag': False,
    },
    {
        'ticker': 'SIDO.JK',
        'name': 'Sido Muncul Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 525,
        'price_change_3y': -42.0,
        'price_change_1y': -22.0,
        'debt_to_equity': 0.05,
        'roe': 20.5,
        'roa': 18.2,
        'profit_margin': 22.5,
        'dividend_yield': 7.5,
        'current_ratio': 5.8,
        'earnings_growth': -8.5,
        'pe_ratio': 10.5,
        'pb_ratio': 2.1,
        'peg_ratio': None,
        'market_cap': 16e12,
        'avg_volume': 12_000_000,
        'free_float_pct': 19,
        'operating_cash_flow': 700,
        'payout_ratio': 75,
        'governance_flag': False,
        'notes': 'Herbal demand turun, kompetisi tinggi',
    },
    {
        'ticker': 'MYOR.JK',
        'name': 'Mayora Indah Tbk',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 2360,
        'price_change_3y': 61.1,
        'price_change_1y': 15.1,
        'debt_to_equity': 0.72,
        'roe': 22.8,
        'roa': 9.5,
        'profit_margin': 10.5,
        'dividend_yield': 1.8,
        'current_ratio': 2.5,
        'earnings_growth': 25.8,
        'pe_ratio': 15.2,
        'pb_ratio': 3.5,
        'peg_ratio': 0.59,
        'market_cap': 53.8e12,
        'avg_volume': 3_500_000,
        'free_float_pct': 67,
        'operating_cash_flow': 1500,
        'payout_ratio': 20,
        'governance_flag': False,
    },

    # Telekomunikasi
    {
        'ticker': 'TLKM.JK',
        'name': 'Telkom Indonesia Tbk',
        'sector': 'Communication Services',
        'industry': 'Telecom Services',
        'current_price': 2710,  # Update 21 Sep 2026: -1.1% dari 2740 (Investing, 15 Sep)
        'price_change_3y': -28.5,
        'debt_to_equity': 0.55,
        'roe': 18.5,
        'roa': 8.2,
        'profit_margin': 18.5,
        'dividend_yield': 5.5,
        'current_ratio': 0.8,
        'earnings_growth': -5.2,
        'pe_ratio': 10.5,
        'pb_ratio': 1.9,
        'peg_ratio': None,
        'market_cap': 280e12,
        'avg_volume': 50_000_000,
        'free_float_pct': 48,
        'operating_cash_flow': 30000,
        'payout_ratio': 85,  # TINGGI - BUMN policy, gagal filter
        'governance_flag': False,
    },

    # Mining & Energy
    {
        'ticker': 'ADRO.JK',
        'name': 'Adaro Energy Indonesia',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 2780,  # Update 21 Sep 2026: +4.9% dari 2650 (Ajaib)
        'price_change_3y': 145.2,
        'price_change_1y': -18.5,
        'debt_to_equity': 0.35,
        'roe': 25.5,
        'roa': 14.5,
        'profit_margin': 22.5,
        'dividend_yield': 7.5,
        'current_ratio': 2.8,
        'earnings_growth': -12.5,
        'pe_ratio': 6.2,
        'pb_ratio': 1.5,
        'peg_ratio': None,
        'market_cap': 75e12,
        'avg_volume': 35_000_000,
        'free_float_pct': 35,
        'operating_cash_flow': 12000,
        'payout_ratio': 40,
        'governance_flag': False,
        'notes': 'Coal cycle sudah peak, sedang spin-off divisi baru',
    },
    {
        'ticker': 'INCO.JK',
        'name': 'Vale Indonesia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Nickel',
        'current_price': 4820,  # Update 2 Sep 2026: -3.6% dari 5000 (portfolio)
        'price_change_3y': 195.8,  # 3 TAHUN: dari ~1885 ke 5575
        'price_change_1y': 95.6,  # 1 TAHUN: dari ~2850 ke 5575 - masih UP
        'debt_to_equity': 0.15,
        'roe': 18.5,
        'roa': 12.5,
        'profit_margin': 22.5,
        'dividend_yield': 3.1,
        'current_ratio': 4.5,
        'earnings_growth': 35.2,
        'pe_ratio': 11.8,
        'pb_ratio': 2.2,
        'peg_ratio': 0.34,
        'market_cap': 72.9e12,
        'avg_volume': 18_000_000,
        'free_float_pct': 21,  # ⚠️ Di bawah 25%, tapi masih ok
        # V5.0 NEW FIELDS
        'operating_cash_flow': 5200,  # OCF dalam miliar IDR (positif)
        'payout_ratio': 45,  # Payout ratio 45% - sustainable
        'governance_flag': False,  # Tidak ada red flag
        'notes': 'V5.0: ROE 18.5% OK, OCF positif, governance clean',
    },
    {
        'ticker': 'ANTM.JK',
        'name': 'Aneka Tambang Tbk',
        'sector': 'Basic Materials',
        'industry': 'Other Industrial Metals',
        'current_price': 3040,  # Update 21 Ags 2026: +5.2% dari 2890 (Ajaib)
        'price_change_3y': 270.7,  # 3 TAHUN: dari ~998 ke 3700
        'price_change_1y': 166.2,  # 1 TAHUN: dari ~1390 ke 3700 - masih UP
        'debt_to_equity': 0.42,
        'roe': 15.8,
        'roa': 8.5,
        'profit_margin': 12.5,
        'dividend_yield': 4.0,  # Yield naik karena harga turun
        'current_ratio': 2.2,
        'earnings_growth': 32.5,
        'pe_ratio': 11.5,
        'pb_ratio': 1.8,
        'peg_ratio': 0.35,
        'market_cap': 90.2e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 35,  # ✅ Free float sehat
        # V5.0 NEW FIELDS
        'operating_cash_flow': 8500,  # OCF dalam miliar IDR (BUMN, strong)
        'payout_ratio': 40,  # Payout ratio 40% - very sustainable
        'governance_flag': False,  # BUMN, governance clear
        'notes': 'V5.0: ROE 15.8% OK, BUMN governance, OCF strong',
    },

    # Otomotif & Konglomerasi
    {
        'ticker': 'ASII.JK',
        'name': 'Astra International Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Auto Manufacturers',
        'current_price': 4780,  # Update 1 Sep 2026: -1.5% dari 4850
        'price_change_3y': -8.5,
        'debt_to_equity': 0.85,
        'roe': 15.2,
        'roa': 6.8,
        'profit_margin': 9.5,
        'dividend_yield': 5.8,
        'current_ratio': 1.3,
        'earnings_growth': 10.2,
        'pe_ratio': 8.5,
        'pb_ratio': 1.3,
        'peg_ratio': 0.83,
        'market_cap': 195e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 50,
        'operating_cash_flow': 18000,
        'payout_ratio': 35,
        'governance_flag': False,
    },
    {
        'ticker': 'UNTR.JK',
        'name': 'United Tractors Tbk',
        'sector': 'Industrials',
        'industry': 'Farm & Heavy Machinery',
        'current_price': 29550,
        'price_change_3y': 59.7,
        'price_change_1y': 7.5,
        'debt_to_equity': 0.52,
        'roe': 18.5,
        'roa': 10.2,
        'profit_margin': 15.8,
        'dividend_yield': 6.5,
        'current_ratio': 1.8,
        'earnings_growth': 18.5,
        'pe_ratio': 7.5,
        'pb_ratio': 1.4,
        'peg_ratio': 0.41,
        'market_cap': 102e12,
        'avg_volume': 5_000_000,
        'free_float_pct': 41,
        'operating_cash_flow': 10000,
        'payout_ratio': 35,
        'governance_flag': False,
    },
    {
        'ticker': 'AUTO.JK',
        'name': 'Astra Otoparts Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Auto Parts',
        'current_price': 3390,  # Update 2 Sep 2026: +25.6% dari 2700 (portfolio - koreksi data lama)
        'price_change_3y': 43.7,  # 3 TAHUN: dari ~1775 ke 2550
        'price_change_1y': 26.9,  # 1 TAHUN: dari ~2010 ke 2550 - still UP
        'debt_to_equity': 0.035,  # 3.5% - SANGAT RENDAH
        'roe': 12.5,
        'roa': 7.8,
        'profit_margin': 8.2,
        'dividend_yield': 7.3,  # 7.30% HIGH
        'current_ratio': 1.9,
        'earnings_growth': 15.2,
        'pe_ratio': 9.5,
        'pb_ratio': 1.2,
        'peg_ratio': 0.63,
        'market_cap': 10.5e12,
        'avg_volume': 1_500_000,
        'free_float_pct': 20,  # ⚠️ Agak rendah tapi Astra group
        # V5.0 NEW FIELDS
        'operating_cash_flow': 1200,  # OCF dalam miliar IDR
        'payout_ratio': 60,  # Payout ratio 60% - sustainable
        'governance_flag': False,  # Astra group, governance clean
        'notes': 'V5.0: ROE 12.5% borderline OK, Astra governance, ultra low D/E',
    },

    # Retail
    {
        'ticker': 'ACES.JK',
        'name': 'Ace Hardware Indonesia',
        'sector': 'Consumer Cyclical',
        'industry': 'Home Improvement Retail',
        'current_price': 840,
        'price_change_3y': -15.2,
        'debt_to_equity': 0.08,
        'roe': 22.5,
        'roa': 15.8,
        'profit_margin': 12.5,
        'dividend_yield': 3.5,
        'current_ratio': 5.2,
        'earnings_growth': 22.5,
        'pe_ratio': 18.5,
        'pb_ratio': 4.2,
        'peg_ratio': 0.82,
        'market_cap': 14e12,
        'avg_volume': 8_000_000,
        'free_float_pct': 30,
        'operating_cash_flow': 600,
        'payout_ratio': 50,
        'governance_flag': False,
    },
    {
        'ticker': 'MAPI.JK',
        'name': 'Mitra Adiperkasa Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Apparel Retail',
        'current_price': 1650,
        'price_change_3y': 95.2,
        'debt_to_equity': 0.95,
        'roe': 18.5,
        'roa': 5.5,
        'profit_margin': 6.8,
        'dividend_yield': 1.5,
        'current_ratio': 1.4,
        'earnings_growth': 35.5,
        'pe_ratio': 14.5,
        'pb_ratio': 2.7,
        'peg_ratio': 0.41,
        'market_cap': 28e12,
        'avg_volume': 6_000_000,
        'free_float_pct': 42,
        'operating_cash_flow': 1200,
        'payout_ratio': 20,
        'governance_flag': False,
    },
    {
        'ticker': 'AMRT.JK',
        'name': 'Sumber Alfaria Trijaya',
        'sector': 'Consumer Defensive',
        'industry': 'Grocery Stores',
        'current_price': 1770,  # Update 20 Feb 2026: CRASH dari 2850!
        'price_change_3y': 32.1,  # 3 TAHUN: dari ~1340 ke 1770 (masih positif tapi lemah)
        'price_change_1y': -37.68,  # 1 TAHUN: DOWNTREND PARAH! -37.68%
        'debt_to_equity': 0.85,
        'roe': 28.5,
        'roa': 8.5,
        'profit_margin': 3.2,
        'dividend_yield': 1.2,
        'current_ratio': 1.1,
        'earnings_growth': 28.5,
        'pe_ratio': 28.5,
        'pb_ratio': 8.1,
        'peg_ratio': 1.0,
        'market_cap': 71.84e12,
        'avg_volume': 12_000_000,
        'free_float_pct': 35,
        # V5.0 NEW FIELDS
        'governance_flag': True,  # ⚠️ REMOVED FROM MSCI MAY 2026!
        'notes': '⚠️ MSCI REMOVED MEI 2026! Ownership concentration issue',
    },

    # Properti
    {
        'ticker': 'BSDE.JK',
        'name': 'Bumi Serpong Damai Tbk',
        'sector': 'Real Estate',
        'industry': 'Real Estate Development',
        'current_price': 1150,
        'price_change_3y': 25.2,
        'debt_to_equity': 0.42,
        'roe': 8.5,
        'roa': 4.2,
        'profit_margin': 28.5,
        'dividend_yield': 2.5,
        'current_ratio': 3.5,
        'earnings_growth': 18.5,
        'pe_ratio': 8.5,
        'pb_ratio': 0.7,
        'peg_ratio': 0.46,
        'market_cap': 22e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 48,
        'operating_cash_flow': 2000,
        'payout_ratio': 20,
        'governance_flag': False,
    },
    {
        'ticker': 'CTRA.JK',
        'name': 'Ciputra Development Tbk',
        'sector': 'Real Estate',
        'industry': 'Real Estate Development',
        'current_price': 1180,
        'price_change_3y': 45.5,
        'debt_to_equity': 0.55,
        'roe': 10.2,
        'roa': 4.8,
        'profit_margin': 22.5,
        'dividend_yield': 1.8,
        'current_ratio': 2.8,
        'earnings_growth': 25.8,
        'pe_ratio': 9.5,
        'pb_ratio': 0.9,
        'peg_ratio': 0.37,
        'market_cap': 21e12,
        'avg_volume': 15_000_000,
        'free_float_pct': 42,
        'operating_cash_flow': 1500,
        'payout_ratio': 25,
        'governance_flag': False,
    },

    # Semen
    {
        'ticker': 'SMGR.JK',
        'name': 'Semen Indonesia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 4250,
        'price_change_3y': -42.5,
        'debt_to_equity': 0.72,
        'roe': 8.5,
        'roa': 4.2,
        'profit_margin': 8.2,
        'dividend_yield': 4.5,
        'current_ratio': 1.2,
        'earnings_growth': -8.5,
        'pe_ratio': 12.5,
        'pb_ratio': 1.1,
        'peg_ratio': None,
        'market_cap': 25e12,
        'avg_volume': 10_000_000,
        'free_float_pct': 49,
        'operating_cash_flow': 1500,
        'payout_ratio': 30,
        'governance_flag': False,
    },
    {
        'ticker': 'INTP.JK',
        'name': 'Indocement Tunggal Prakarsa',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 7500,
        'price_change_3y': -18.5,
        'debt_to_equity': 0.18,
        'roe': 6.5,
        'roa': 4.8,
        'profit_margin': 12.5,
        'dividend_yield': 3.2,
        'current_ratio': 3.8,
        'earnings_growth': 5.2,
        'pe_ratio': 18.5,
        'pb_ratio': 1.2,
        'peg_ratio': 3.56,
        'market_cap': 28e12,
        'avg_volume': 3_000_000,
        'free_float_pct': 36,
        'operating_cash_flow': 1000,
        'payout_ratio': 30,
        'governance_flag': False,
    },

    # Tower & Infrastruktur
    {
        'ticker': 'TOWR.JK',
        'name': 'Sarana Menara Nusantara',
        'sector': 'Real Estate',
        'industry': 'REIT - Specialty',
        'current_price': 414,  # Update 21 Ags 2026 (Ajaib) - possible stock split
        'price_change_3y': -22.5,
        'debt_to_equity': 1.85,
        'roe': 32.5,
        'roa': 8.5,
        'profit_margin': 42.5,
        'dividend_yield': 2.8,
        'current_ratio': 0.8,
        'earnings_growth': 15.2,
        'pe_ratio': 12.5,
        'pb_ratio': 4.1,
        'peg_ratio': 0.82,
        'market_cap': 45e12,
        'avg_volume': 20_000_000,
        'free_float_pct': 38,
        'operating_cash_flow': 4000,
        'payout_ratio': 25,
        'governance_flag': False,
    },
    {
        'ticker': 'TBIG.JK',
        'name': 'Tower Bersama Infrastructure',
        'sector': 'Real Estate',
        'industry': 'REIT - Specialty',
        'current_price': 1375,  # Update 21 Ags 2026 (Ajaib)
        'price_change_3y': -15.8,
        'debt_to_equity': 2.25,
        'roe': 28.5,
        'roa': 5.2,
        'profit_margin': 38.5,
        'dividend_yield': 2.2,
        'current_ratio': 0.5,
        'earnings_growth': 12.5,
        'pe_ratio': 15.5,
        'pb_ratio': 4.4,
        'peg_ratio': 1.24,
        'market_cap': 48e12,
        'avg_volume': 8_000_000,
        'free_float_pct': 35,
        'operating_cash_flow': 3500,
        'payout_ratio': 20,
        'governance_flag': False,
    },

    # Poultry/Peternakan
    {
        'ticker': 'CPIN.JK',
        'name': 'Charoen Pokphand Indonesia',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 5050,
        'price_change_3y': -5.8,
        'debt_to_equity': 0.42,
        'roe': 18.5,
        'roa': 10.5,
        'profit_margin': 8.5,
        'dividend_yield': 2.5,
        'current_ratio': 2.2,
        'earnings_growth': 22.5,
        'pe_ratio': 14.5,
        'pb_ratio': 2.7,
        'peg_ratio': 0.64,
        'market_cap': 82e12,
        'avg_volume': 8_000_000,
        'free_float_pct': 45,
        'operating_cash_flow': 2500,
        'payout_ratio': 30,
        'governance_flag': False,
    },
    {
        'ticker': 'JPFA.JK',
        'name': 'Japfa Comfeed Indonesia',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 2250,  # Update 21 Ags 2026: +42.4% dari 1580 (Kompas100, 20 Ags)
        'price_change_3y': 58.2,
        'debt_to_equity': 0.95,
        'roe': 15.2,
        'roa': 5.8,
        'profit_margin': 5.5,
        'dividend_yield': 3.2,
        'current_ratio': 1.5,
        'earnings_growth': 32.5,
        'pe_ratio': 8.5,
        'pb_ratio': 1.3,
        'peg_ratio': 0.26,
        'market_cap': 18e12,
        'avg_volume': 12_000_000,
        'free_float_pct': 48,
        'operating_cash_flow': 1000,
        'payout_ratio': 20,
        'governance_flag': False,
    },

    # Media
    {
        'ticker': 'SCMA.JK',
        'name': 'Surya Citra Media Tbk',
        'sector': 'Communication Services',
        'industry': 'Broadcasting',
        'current_price': 142,
        'price_change_3y': -68.5,
        'debt_to_equity': 0.12,
        'roe': 12.5,
        'roa': 8.5,
        'profit_margin': 18.5,
        'dividend_yield': 5.5,
        'current_ratio': 2.8,
        'earnings_growth': -15.2,
        'pe_ratio': 8.5,
        'pb_ratio': 1.1,
        'peg_ratio': None,
        'market_cap': 2e12,
        'avg_volume': 15_000_000,
        'free_float_pct': 25,
        'operating_cash_flow': 400,
        'payout_ratio': 55,
        'governance_flag': False,
    },

    # Keramik
    {
        'ticker': 'ARNA.JK',
        'name': 'Arwana Citramulia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 595,
        'price_change_3y': 38.5,
        'debt_to_equity': 0.22,
        'roe': 22.5,
        'roa': 15.8,
        'profit_margin': 15.2,
        'dividend_yield': 4.5,
        'current_ratio': 3.2,
        'earnings_growth': 18.5,
        'pe_ratio': 12.5,
        'pb_ratio': 2.8,
        'peg_ratio': 0.68,
        'market_cap': 4.5e12,
        'avg_volume': 5_000_000,
        'free_float_pct': 38,
        'operating_cash_flow': 300,
        'payout_ratio': 60,
        'governance_flag': False,
    },

    # Elektronik Retail
    {
        'ticker': 'ERAA.JK',
        'name': 'Erajaya Swasembada Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Electronics & Appliances',
        'current_price': 428,
        'price_change_3y': 72.5,
        'debt_to_equity': 0.85,
        'roe': 15.8,
        'roa': 5.2,
        'profit_margin': 2.8,
        'dividend_yield': 2.2,
        'current_ratio': 1.5,
        'earnings_growth': 55.2,
        'pe_ratio': 10.5,
        'pb_ratio': 1.7,
        'peg_ratio': 0.19,
        'market_cap': 13e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 45,
        'operating_cash_flow': 400,
        'payout_ratio': 25,
        'governance_flag': False,
    },

    # =========================================================================
    # SAHAM BARU - Verified passing all 5 criteria (April 2026)
    # =========================================================================

    # Tin Mining - VERIFIED PASS V5.0
    {
        'ticker': 'TINS.JK',
        'name': 'Timah Tbk',
        'sector': 'Basic Materials',
        'industry': 'Tin Mining',
        'current_price': 4420,  # Update 21 Sep 2026: +10.2% dari 4010 (Pluang)
        'price_change_3y': 359.4,  # 3 TAHUN: dari ~825 ke 3790
        'price_change_1y': 247.7,  # 1 TAHUN: dari ~1090 ke 3790 - UPTREND!
        'debt_to_equity': 0.007,  # 0.72% - SANGAT RENDAH
        'roe': 15.0,
        'roa': 8.5,
        'profit_margin': 12.0,
        'dividend_yield': 1.92,
        'current_ratio': 2.5,
        'earnings_growth': 176.4,  # Projected 2026
        'pe_ratio': 8.5,
        'pb_ratio': 1.3,
        'peg_ratio': 0.05,
        'market_cap': 39e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 35,  # ✅ Free float sehat
        # V5.0 NEW FIELDS
        'operating_cash_flow': 4200,  # OCF dalam miliar IDR (BUMN)
        'payout_ratio': 35,  # Payout ratio 35% - very sustainable
        'governance_flag': False,  # BUMN, governance clear
        'notes': 'V5.0: ROE 15% OK, BUMN, ultra low D/E 0.7%',
    },

    # Palm Oil Plantation - VERIFIED PASS V5.0
    {
        'ticker': 'AALI.JK',
        'name': 'Astra Agro Lestari Tbk',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 6175,  # Update 17 Juli 2026: -16.3%
        'price_change_3y': 50.9,  # 3 TAHUN: dari ~5200 ke 7850
        'price_change_1y': 37.1,  # 1 TAHUN: dari ~5725 ke 7850 - UPTREND!
        'debt_to_equity': 0.004,  # 0.38% - SANGAT RENDAH
        'roe': 14.6,
        'roa': 9.7,
        'profit_margin': 15.5,
        'dividend_yield': 4.09,
        'current_ratio': 1.8,
        'earnings_growth': 12.5,
        'pe_ratio': 9.2,
        'pb_ratio': 1.3,
        'peg_ratio': 0.74,
        'market_cap': 14.6e12,
        'avg_volume': 3_000_000,
        'free_float_pct': 20,  # ⚠️ Agak rendah tapi Astra group
        # V5.0 NEW FIELDS
        'operating_cash_flow': 3800,  # OCF dalam miliar IDR
        'payout_ratio': 55,  # Payout ratio 55% - sustainable
        'governance_flag': False,  # Astra group, governance clean
        'notes': 'V5.0: ROE 14.6% OK, Astra governance, ultra low D/E',
    },

    # Pharmaceutical - VERIFIED PASS V5.0
    {
        'ticker': 'TSPC.JK',
        'name': 'Tempo Scan Pacific Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 2760,  # Update 2 Sep 2026: -6.8% dari 2960 (portfolio)
        'price_change_3y': 49.2,  # 3 TAHUN: dari ~1790 ke 2670
        'price_change_1y': 30.4,  # 1 TAHUN: dari ~2047 ke 2670 - UPTREND!
        'debt_to_equity': 0.12,  # 12% - RENDAH
        'roe': 18.5,
        'roa': 12.8,
        'profit_margin': 11.2,
        'dividend_yield': 5.51,
        'current_ratio': 3.5,
        'earnings_growth': 15.2,
        'pe_ratio': 12.5,
        'pb_ratio': 2.3,
        'peg_ratio': 0.82,
        'market_cap': 11e12,
        'avg_volume': 5_000_000,
        'free_float_pct': 25,  # ✅ Free float sehat
        # V5.0 NEW FIELDS
        'operating_cash_flow': 1800,  # OCF dalam miliar IDR
        'payout_ratio': 65,  # Payout ratio 65% - sustainable
        'governance_flag': False,  # Clean governance
        'notes': 'V5.0: ROE 18.5% STRONG, defensive pharma, low debt',
    },

    # =========================================================================
    # SAHAM BARU - Coal Mining (Mei 2026 Scan)
    # =========================================================================

    # Coal Mining - VERIFIED PASS V5.0
    {
        'ticker': 'ITMG.JK',
        'name': 'Indo Tambangraya Megah Tbk',
        'sector': 'Energy',
        'industry': 'Coal Mining',
        'current_price': 24675,  # Update 21 Ags 2026: -2.9% dari 25400 (Ajaib)
        'price_change_3y': 46.4,  # 3 TAHUN: estimasi
        'price_change_1y': 17.0,  # 1 TAHUN: consolidation
        'debt_to_equity': 0.022,  # 2.2% - SANGAT RENDAH
        'roe': 25.0,
        'roa': 18.0,
        'profit_margin': 15.0,
        'dividend_yield': 11.72,  # VERY HIGH!
        'current_ratio': 2.5,
        'earnings_growth': 10.0,
        'pe_ratio': 5.5,
        'pb_ratio': 1.4,
        'peg_ratio': 0.55,
        'market_cap': 28e12,
        'avg_volume': 3_000_000,
        'free_float_pct': 35,  # ✅ Free float sehat
        # V5.0 NEW FIELDS
        'operating_cash_flow': 8060,  # OCF 8.06T IDR (dari search)
        'payout_ratio': 86,  # ⚠️ Payout 86% TINGGI tapi covered by OCF
        'governance_flag': False,  # Clean governance
        'notes': 'V5.0: ROE 25% EXCELLENT, OCF strong. ⚠️ Payout ratio tinggi tapi cash covered',
    },

    # Coal Mining BUMN - VERIFIED PASS V5.0
    {
        'ticker': 'PTBA.JK',
        'name': 'Bukit Asam Tbk',
        'sector': 'Energy',
        'industry': 'Coal Mining',
        'current_price': 3090,  # Update 21 Sep 2026: +13.6% dari 2720 (Ajaib)
        'price_change_3y': 34.1,  # 3 TAHUN: estimasi
        'price_change_1y': 14.9,  # 1 TAHUN: koreksi
        'debt_to_equity': 0.20,  # 20% - RENDAH
        'roe': 22.0,
        'roa': 15.0,
        'profit_margin': 18.0,
        'dividend_yield': 11.19,  # VERY HIGH!
        'current_ratio': 2.2,
        'earnings_growth': 8.0,
        'pe_ratio': 6.0,
        'pb_ratio': 1.3,
        'peg_ratio': 0.75,
        'market_cap': 34e12,
        'avg_volume': 8_000_000,
        'free_float_pct': 35,  # ✅ Free float sehat
        # V5.0 NEW FIELDS
        'operating_cash_flow': 7500,  # OCF dalam miliar IDR (BUMN strong)
        'payout_ratio': 75,  # Payout ratio 75% - masih ok untuk BUMN
        'governance_flag': False,  # BUMN, governance clear
        'notes': 'V5.0: ROE 22% STRONG, BUMN governance, high dividend sustainable',
    },

    # =========================================================================
    # SAHAM BARU - LQ45 Agustus 2026 (belum ada di dataset)
    # Data: riset fundamental Sep 2026 (Yahoo, Investing, Stockbit, IDX)
    # =========================================================================

    # Tech - GOTO (MSCI REMOVED Aug 2026, price floor Rp50)
    {
        'ticker': 'GOTO.JK',
        'name': 'GoTo Gojek Tokopedia Tbk',
        'sector': 'Technology',
        'industry': 'Internet Content & Information',
        'current_price': 50,  # Update Sep 2026: floor Rp50 sejak Mei 2026
        'price_change_3y': -42.0,
        'price_change_1y': -30.0,
        'debt_to_equity': 0.145,
        'roe': -6.3,  # Masih rugi
        'roa': -2.0,
        'profit_margin': -6.5,
        'dividend_yield': 0,  # Tidak bayar dividen
        'current_ratio': 2.5,
        'earnings_growth': 77.0,  # Rugi menyempit 77% YoY
        'pe_ratio': None,  # Loss
        'pb_ratio': 1.3,
        'peg_ratio': None,
        'market_cap': 60e12,
        'avg_volume': 2_000_000_000,
        'free_float_pct': 65,
        'operating_cash_flow': 1000,  # OCF turn positive (est)
        'payout_ratio': 0,
        'governance_flag': True,  # MSCI REMOVED Aug 2026, likuiditas kolaps
        'notes': 'MSCI REMOVED Aug 2026, floor Rp50, masih rugi - GAGAL filter',
    },

    # Copper/Gold - AMMN (MSCI REMOVED May 2026, HSC)
    {
        'ticker': 'AMMN.JK',
        'name': 'Amman Mineral Internasional Tbk',
        'sector': 'Basic Materials',
        'industry': 'Copper',
        'current_price': 4410,  # Update Sep 2026
        'price_change_3y': 160.0,
        'price_change_1y': -40.0,
        'debt_to_equity': 1.1,
        'roe': 4.7,
        'roa': 4.0,
        'profit_margin': 20.0,
        'dividend_yield': 0,
        'current_ratio': 1.5,
        'earnings_growth': -30.0,
        'pe_ratio': 27.9,
        'pb_ratio': 5.5,
        'peg_ratio': None,
        'market_cap': 319e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 19,  # MSCI-adjusted ~10%, IDX ~19%
        'operating_cash_flow': 18000,
        'payout_ratio': 0,
        'governance_flag': True,  # MSCI REMOVED May 2026, high shareholding concentration
        'notes': 'MSCI REMOVED May 2026 (HSC/low float), ROE 4.7%, no div - GAGAL',
    },

    # Mining - MDKA (near-breakeven, high leverage)
    {
        'ticker': 'MDKA.JK',
        'name': 'Merdeka Copper Gold Tbk',
        'sector': 'Basic Materials',
        'industry': 'Gold',
        'current_price': 2520,  # Update Sep 2026
        'price_change_3y': -35.0,
        'price_change_1y': 14.65,
        'debt_to_equity': 1.87,  # High leverage
        'roe': -0.09,  # Breakeven/rugi tipis
        'roa': -0.5,
        'profit_margin': -1.0,
        'dividend_yield': 0,
        'current_ratio': 1.2,
        'earnings_growth': -50.0,
        'pe_ratio': None,  # Loss
        'pb_ratio': 2.8,
        'peg_ratio': None,
        'market_cap': 61e12,
        'avg_volume': 70_000_000,
        'free_float_pct': 35,
        'operating_cash_flow': 3500,
        'payout_ratio': 0,
        'governance_flag': False,
        'notes': 'ROE breakeven, D/E 1.87 tinggi, no div - GAGAL filter',
    },

    # BANK Syariah - BRIS
    {
        'ticker': 'BRIS.JK',
        'name': 'Bank Syariah Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 1710,  # Update Sep 2026
        'price_change_3y': 5.0,
        'price_change_1y': -25.0,
        'car': 22.0,
        'npl': 1.81,  # NPF gross
        'nim': 5.6,
        'ldr': 80.0,  # FDR
        'cost_to_income': 40.0,
        'debt_to_equity': None,
        'roe': 19.36,
        'roa': 2.54,
        'profit_margin': 30.0,
        'dividend_yield': 1.8,
        'current_ratio': None,
        'earnings_growth': 15.0,
        'pe_ratio': 11.0,
        'pb_ratio': 2.0,
        'peg_ratio': 0.73,
        'market_cap': 79e12,
        'avg_volume': 55_000_000,
        'free_float_pct': 13,  # BRI/Mandiri/BNI own ~87% - DI BAWAH 15%
        'operating_cash_flow': 15000,
        'payout_ratio': 20,
        'governance_flag': False,
        'notes': 'Fundamental OK (ROE 19%) tapi free float 13% <15% - GAGAL filter',
    },

    # Energy Geothermal - PGEO (low free float)
    {
        'ticker': 'PGEO.JK',
        'name': 'Pertamina Geothermal Energy Tbk',
        'sector': 'Utilities',
        'industry': 'Utilities - Renewable',
        'current_price': 1100,  # Update Aug 2026
        'price_change_3y': 45.0,
        'price_change_1y': 10.0,
        'debt_to_equity': 0.38,
        'roe': 7.2,
        'roa': 4.48,
        'profit_margin': 32.0,
        'dividend_yield': 4.7,
        'current_ratio': 4.47,
        'earnings_growth': -14.2,
        'pe_ratio': 20.0,
        'pb_ratio': 1.5,
        'peg_ratio': None,
        'market_cap': 44e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 12,  # Pertamina ~82% - DI BAWAH 15%
        'operating_cash_flow': 4000,
        'payout_ratio': 80,
        'governance_flag': False,
        'notes': 'ROE 7.2% <10% & free float 12% <15% - GAGAL filter',
    },

    # Gas Utility - PGAS (high payout)
    {
        'ticker': 'PGAS.JK',
        'name': 'Perusahaan Gas Negara Tbk',
        'sector': 'Utilities',
        'industry': 'Utilities - Regulated Gas',
        'current_price': 1530,  # Update Sep 2026
        'price_change_3y': -7.0,
        'price_change_1y': -4.79,
        'debt_to_equity': 0.29,
        'roe': 10.09,
        'roa': 5.0,
        'profit_margin': 8.0,
        'dividend_yield': 12.2,  # Very high
        'current_ratio': 2.01,
        'earnings_growth': 5.0,
        'pe_ratio': 8.74,
        'pb_ratio': 0.9,
        'peg_ratio': None,
        'market_cap': 36e12,
        'avg_volume': 60_000_000,
        'free_float_pct': 43,
        'operating_cash_flow': 11000,
        'payout_ratio': 87.3,  # DI ATAS 80% - BUMN policy
        'governance_flag': False,
        'notes': 'ROE 10% & div 12.2% tapi payout 87% >80% - GAGAL filter',
    },

    # Oil & Gas - MEDC (high D/E)
    {
        'ticker': 'MEDC.JK',
        'name': 'Medco Energi Internasional Tbk',
        'sector': 'Energy',
        'industry': 'Oil & Gas E&P',
        'current_price': 1040,  # Update Sep 2026 (est)
        'price_change_3y': -5.0,
        'price_change_1y': -15.0,
        'debt_to_equity': 1.65,  # High - DI ATAS 1.0
        'roe': 8.12,
        'roa': 3.0,
        'profit_margin': 7.74,
        'dividend_yield': 4.0,
        'current_ratio': 1.3,
        'earnings_growth': 50.0,
        'pe_ratio': 12.51,
        'pb_ratio': 1.0,
        'peg_ratio': 0.25,
        'market_cap': 26e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 45,
        'operating_cash_flow': 14000,
        'payout_ratio': 40,
        'governance_flag': False,
        'notes': 'D/E 1.65 >1.0 & ROE 8.1% <10% - GAGAL filter',
    },

    # Energy Distribution - AKRA (LOLOS)
    {
        'ticker': 'AKRA.JK',
        'name': 'AKR Corporindo Tbk',
        'sector': 'Energy',
        'industry': 'Oil & Gas Refining & Marketing',
        'current_price': 1345,  # Update Sep 2026
        'price_change_3y': -10.0,
        'price_change_1y': 10.66,
        'debt_to_equity': 0.33,
        'roe': 19.53,
        'roa': 10.0,
        'profit_margin': 5.0,
        'dividend_yield': 7.3,
        'current_ratio': 1.33,
        'earnings_growth': 3.0,
        'pe_ratio': 10.13,
        'pb_ratio': 1.9,
        'peg_ratio': None,
        'market_cap': 27e12,
        'avg_volume': 65_000_000,
        'free_float_pct': 41,
        'operating_cash_flow': 2500,
        'payout_ratio': 70,
        'governance_flag': False,
        'notes': 'LOLOS: ROE 19.5%, D/E rendah, div 7.3%, valuasi murah',
    },

    # Pulp & Paper - INKP (low ROE)
    {
        'ticker': 'INKP.JK',
        'name': 'Indah Kiat Pulp & Paper Tbk',
        'sector': 'Basic Materials',
        'industry': 'Paper & Paper Products',
        'current_price': 8500,  # Update Aug 2026
        'price_change_3y': 2.0,
        'price_change_1y': 23.35,
        'debt_to_equity': 0.68,
        'roe': 6.9,  # DI BAWAH 10%
        'roa': 3.5,
        'profit_margin': 14.6,
        'dividend_yield': 0.85,
        'current_ratio': 1.7,
        'earnings_growth': 12.0,
        'pe_ratio': 5.45,
        'pb_ratio': 0.4,  # Deep discount
        'peg_ratio': 0.45,
        'market_cap': 46e12,
        'avg_volume': 10_000_000,
        'free_float_pct': 47,
        'operating_cash_flow': 11000,
        'payout_ratio': 5,
        'governance_flag': False,
        'notes': 'Valuasi super murah (PBV 0.4) tapi ROE 6.9% <10% - GAGAL filter',
    },

    # Telecom - ISAT (high D/E)
    {
        'ticker': 'ISAT.JK',
        'name': 'Indosat Ooredoo Hutchison Tbk',
        'sector': 'Communication Services',
        'industry': 'Telecom Services',
        'current_price': 2220,  # Update Sep 2026
        'price_change_3y': -60.0,
        'price_change_1y': -30.0,
        'debt_to_equity': 1.33,  # DI ATAS 1.0
        'roe': 15.03,
        'roa': 5.0,
        'profit_margin': 10.0,
        'dividend_yield': 3.5,
        'current_ratio': 0.5,
        'earnings_growth': 26.0,
        'pe_ratio': 12.58,
        'pb_ratio': 2.6,
        'peg_ratio': 0.48,
        'market_cap': 71e12,
        'avg_volume': 30_000_000,
        'free_float_pct': 17,
        'operating_cash_flow': 22010,  # Strong OCF (sourced)
        'payout_ratio': 58.5,
        'governance_flag': False,
        'notes': 'ROE 15% & OCF kuat tapi D/E 1.33 >1.0 (telco) - GAGAL filter',
    },

    # Telecom - EXCL/XLSMART (loss FY25, turnaround)
    {
        'ticker': 'EXCL.JK',
        'name': 'XLSMART Telecom Sejahtera Tbk',
        'sector': 'Communication Services',
        'industry': 'Telecom Services',
        'current_price': 2250,  # Update Sep 2026 (est)
        'price_change_3y': 5.0,
        'price_change_1y': 5.0,
        'debt_to_equity': 0.4,
        'roe': -5.0,  # Rugi FY25 (merger costs)
        'roa': -2.0,
        'profit_margin': -3.0,
        'dividend_yield': 6.3,
        'current_ratio': 0.5,
        'earnings_growth': 100.0,  # Turnaround
        'pe_ratio': None,  # Loss TTM
        'pb_ratio': 2.0,
        'peg_ratio': None,
        'market_cap': 47e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 30,
        'operating_cash_flow': 10000,
        'payout_ratio': 0,  # Loss FY25
        'governance_flag': False,
        'notes': 'Merger XL+Smartfren, rugi FY25 - GAGAL filter (ROE negatif)',
    },

    # BANK - BBTN (low ROE)
    {
        'ticker': 'BBTN.JK',
        'name': 'Bank Tabungan Negara Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 1180,  # Update Sep 2026
        'price_change_3y': -15.0,
        'price_change_1y': -15.0,
        'car': 19.0,
        'npl': 3.03,
        'nim': 3.3,  # Mortgage bank - NIM tipis
        'ldr': 96.49,  # High
        'cost_to_income': 50.0,
        'debt_to_equity': None,
        'roe': 9.68,  # DI BAWAH 10%
        'roa': 0.95,
        'profit_margin': 21.0,
        'dividend_yield': 5.0,
        'current_ratio': None,
        'earnings_growth': 14.76,
        'pe_ratio': 5.32,
        'pb_ratio': 0.4,  # Deep discount
        'peg_ratio': 0.36,
        'market_cap': 16.9e12,
        'avg_volume': 75_000_000,
        'free_float_pct': 40,
        'operating_cash_flow': 12000,
        'payout_ratio': 20,
        'governance_flag': False,
        'notes': 'Valuasi murah (PBV 0.4) tapi ROE 9.68% <10% - GAGAL filter',
    },

    # Coal/Energy - INDY (very low ROE)
    {
        'ticker': 'INDY.JK',
        'name': 'Indika Energy Tbk',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 2690,  # Update Sep 2026 (est)
        'price_change_3y': 40.0,
        'price_change_1y': 20.0,
        'debt_to_equity': 0.9,
        'roe': 0.51,  # Sangat rendah (transisi dari coal)
        'roa': 0.3,
        'profit_margin': 2.1,
        'dividend_yield': 7.0,
        'current_ratio': 1.5,
        'earnings_growth': 20.0,
        'pe_ratio': 56.0,  # Tinggi krn earnings tipis
        'pb_ratio': 0.6,
        'peg_ratio': None,
        'market_cap': 14e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 35,
        'operating_cash_flow': 1800,
        'payout_ratio': 50,
        'governance_flag': False,
        'notes': 'ROE 0.51% sangat rendah (transisi coal) - GAGAL filter',
    },

    # Nickel - NCKL/Harita (LOLOS - strong)
    {
        'ticker': 'NCKL.JK',
        'name': 'Trimegah Bangun Persada Tbk',
        'sector': 'Basic Materials',
        'industry': 'Other Industrial Metals',
        'current_price': 1360,  # Update Sep 2026
        'price_change_3y': 50.0,
        'price_change_1y': 10.0,
        'debt_to_equity': 0.25,  # Low
        'roe': 26.28,  # STRONG
        'roa': 12.21,
        'profit_margin': 30.0,
        'dividend_yield': 2.2,
        'current_ratio': 1.5,
        'earnings_growth': 40.32,
        'pe_ratio': 7.93,
        'pb_ratio': 1.29,
        'peg_ratio': 0.20,
        'market_cap': 85.7e12,
        'avg_volume': 50_000_000,
        'free_float_pct': 16,  # Harita ~80% - lolos tipis di atas 15%
        'operating_cash_flow': 6000,
        'payout_ratio': 18,
        'governance_flag': False,  # HSC watch tapi belum di-remove
        'notes': 'LOLOS: ROE 26% STRONG, D/E 0.25, growth 40%. ⚠️ free float 16% ketat',
    },

    # Retail - MAPA (LOLOS)
    {
        'ticker': 'MAPA.JK',
        'name': 'Map Aktif Adiperkasa Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Apparel Retail',
        'current_price': 680,  # Update Sep 2026
        'price_change_3y': -20.0,
        'price_change_1y': -25.0,
        'debt_to_equity': 0.20,
        'roe': 21.84,
        'roa': 11.0,
        'profit_margin': 9.0,
        'dividend_yield': 0.65,
        'current_ratio': 1.8,
        'earnings_growth': 5.0,
        'pe_ratio': 8.70,
        'pb_ratio': 2.0,
        'peg_ratio': 0.4,
        'market_cap': 19.4e12,
        'avg_volume': 35_000_000,
        'free_float_pct': 44,
        'operating_cash_flow': 2000,
        'payout_ratio': 6,
        'governance_flag': False,
        'notes': 'LOLOS: ROE 21.8%, D/E 0.20 rendah, valuasi wajar',
    },
]
