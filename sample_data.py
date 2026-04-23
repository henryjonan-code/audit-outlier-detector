"""
Sample Data Saham IHSG untuk Demonstrasi
Version 4.2 - Update 23 April 2026

============================================================================
DISCLAIMER PENTING:
============================================================================
Data diupdate berdasarkan harga pasar 23 April 2026.

IHSG: ~7,600
Context: Mining stocks volatile, TINS +7.65%, ANTM +2%

Sumber: Yahoo Finance, Investing.com, Katadata
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
        'current_price': 6475,  # Update 23 Apr 2026
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
        'notes': 'Turun 24% YoY - DOWNTREND meski fundamental bagus',
    },
    {
        'ticker': 'BBRI.JK',
        'name': 'Bank Rakyat Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 3430,  # Update 17 Apr 2026: +0.59%
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
        'notes': 'DOWNTREND 3Y! Div yield 9.21% tapi harga turun terus',
    },
    {
        'ticker': 'BMRI.JK',
        'name': 'Bank Mandiri Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 5375,  # Update 25 Feb 2026: RECOVERY! +0.95% hari ini
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
        'notes': 'RECOVERY! +6.93% bulanan, +3.52% weekly - masih DOWNTREND 1Y tapi membaik',
    },
    {
        'ticker': 'BBNI.JK',
        'name': 'Bank Negara Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks',
        'is_bank': True,
        'current_price': 4850,
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
        'notes': '3Y uptrend tapi 1Y downtrend - MIXED SIGNAL',
    },

    # Consumer Goods
    {
        'ticker': 'ICBP.JK',
        'name': 'Indofood CBP Sukses Makmur',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 8150,  # Update 11 Feb 2026: range 8100-8250
        'price_change_3y': 8.2,  # 3 TAHUN: dari ~7530 ke 8150
        'price_change_1y': -31.0,  # 1 TAHUN: TURUN dari 12000 - 52w range: 8050-12000
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
    },
    {
        'ticker': 'INDF.JK',
        'name': 'Indofood Sukses Makmur',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 6800,
        'price_change_3y': 35.2,  # 3 TAHUN
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
    },
    {
        'ticker': 'KLBF.JK',
        'name': 'Kalbe Farma Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 1620,
        'price_change_3y': 12.5,  # 3 TAHUN: relatively flat
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
    },
    {
        'ticker': 'SIDO.JK',
        'name': 'Sido Muncul Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 525,  # FIXED: Harga aktual Feb 2025
        'price_change_3y': -42.0,  # 3 TAHUN: TURUN dari ~900 (2022) ke 525 - DOWNTREND!
        'price_change_1y': -22.0,  # 1 TAHUN: TURUN - DOWNTREND!
        'debt_to_equity': 0.05,
        'roe': 20.5,  # Turun karena revenue pressure
        'roa': 18.2,
        'profit_margin': 22.5,
        'dividend_yield': 7.5,  # Yield naik karena harga turun
        'current_ratio': 5.8,
        'earnings_growth': -8.5,  # NEGATIF
        'pe_ratio': 10.5,
        'pb_ratio': 2.1,
        'peg_ratio': None,  # Negative growth
        'market_cap': 16e12,
        'avg_volume': 12_000_000,
        'free_float_pct': 19,
        'notes': 'Herbal demand turun, kompetisi tinggi',
    },
    {
        'ticker': 'MYOR.JK',
        'name': 'Mayora Indah Tbk',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 2360,  # Update 25 Feb 2026 CLOSING: +2.17%, mcap Rp49.7T
        'price_change_3y': 61.1,  # 3 TAHUN: dari ~1465 ke 2360
        'price_change_1y': 15.1,  # 1 TAHUN: naik dari 6.3% ke 15.1% - KUAT!
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
        'notes': 'Update 25 Feb closing: +2.17%, saham konsumer unjuk gigi saat IHSG naik',
    },

    # Telekomunikasi
    {
        'ticker': 'TLKM.JK',
        'name': 'Telkom Indonesia Tbk',
        'sector': 'Communication Services',
        'industry': 'Telecom Services',
        'current_price': 3230,  # Update 17 Apr 2026: +5.90%
        'price_change_3y': -28.5,  # 3 TAHUN: TURUN SIGNIFIKAN dari ~4000
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
    },

    # Mining & Energy - STARS!
    {
        'ticker': 'ADRO.JK',
        'name': 'Adaro Energy Indonesia',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 2380,  # FIXED: Harga aktual Feb 2025, turun dari peak 3500
        'price_change_3y': 145.2,  # 3 TAHUN: dari ~970 (Feb 2022) - masih positif tapi koreksi
        'price_change_1y': -18.5,  # 1 TAHUN: TURUN dari ~2920 - DOWNTREND!
        'debt_to_equity': 0.35,
        'roe': 25.5,  # Turun dari peak
        'roa': 14.5,
        'profit_margin': 22.5,  # Margin menyusut
        'dividend_yield': 7.5,
        'current_ratio': 2.8,
        'earnings_growth': -12.5,  # NEGATIF: Earnings turun YoY
        'pe_ratio': 6.2,
        'pb_ratio': 1.5,
        'peg_ratio': None,  # Negative growth
        'market_cap': 75e12,
        'avg_volume': 35_000_000,
        'free_float_pct': 35,
        'notes': 'Coal cycle sudah peak, sedang spin-off divisi baru',
    },
    {
        'ticker': 'ITMG.JK',
        'name': 'Indo Tambangraya Megah',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 22100,  # Update 11 Feb 2026: range 22050-22175
        'price_change_3y': 84.2,   # 3 TAHUN: dari ~12000
        'price_change_1y': -21.0,  # 1 TAHUN: TURUN 21% YoY
        'debt_to_equity': 0.25,
        'roe': 32.5,
        'roa': 20.5,
        'profit_margin': 16.5,
        'dividend_yield': 10.03,  # Potensi div yield 10%
        'current_ratio': 3.2,
        'earnings_growth': -12.5,
        'pe_ratio': 5.8,
        'pb_ratio': 1.9,
        'peg_ratio': None,
        'market_cap': 25e12,
        'avg_volume': 2_500_000,
        'free_float_pct': 35,
        'notes': 'Strong coal name, swing trade priority Feb-Mei 2026',
    },
    {
        'ticker': 'PTBA.JK',
        'name': 'Bukit Asam Tbk',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 2300,  # Update 25 Feb 2026 CLOSING: range 2280-2310 - DROP!
        'price_change_3y': 43.8,  # 3 TAHUN: dari ~1600 ke 2300 (turun dari 60%)
        'price_change_1y': -14.0,  # 1 TAHUN: -14%! 52w range: 2170-3070
        'debt_to_equity': 0.28,
        'roe': 25.5,
        'roa': 15.5,
        'profit_margin': 18.5,
        'dividend_yield': 13.04,  # Div yield TTM 13.04% (tapi harga makin turun)
        'current_ratio': 2.5,
        'earnings_growth': -15.5,
        'pe_ratio': 6.3,
        'pb_ratio': 1.6,
        'peg_ratio': None,
        'market_cap': 26.5e12,
        'avg_volume': 15_000_000,
        'free_float_pct': 35,
        'notes': 'AWAS: -14% 1Y! Hampir masuk value trap. 3Y hanya 44% (butuh >50%)',
    },
    {
        'ticker': 'INCO.JK',
        'name': 'Vale Indonesia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Nickel',
        'current_price': 5575,  # Update 23 Apr 2026: koreksi -19%
        'price_change_3y': 195.8,  # 3 TAHUN: dari ~1885 ke 5575
        'price_change_1y': 95.6,  # 1 TAHUN: dari ~2850 ke 5575 - masih UPTREND
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
        'free_float_pct': 21,
        'notes': 'Update 17 Apr: Rebound +24% dari low Maret',
    },
    {
        'ticker': 'ANTM.JK',
        'name': 'Aneka Tambang Tbk',
        'sector': 'Basic Materials',
        'industry': 'Other Industrial Metals',
        'current_price': 4100,  # Update 23 Apr 2026: +5.1%
        'price_change_3y': 310.8,  # 3 TAHUN: dari ~998 ke 4100
        'price_change_1y': 195.0,  # 1 TAHUN: dari ~1390 ke 4100 - UPTREND!
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
        'free_float_pct': 35,
        'notes': 'Update 26 Mar: Koreksi dari ATH 4970, 52w range 1390-4970',
    },

    # Otomotif & Konglomerasi
    {
        'ticker': 'ASII.JK',
        'name': 'Astra International Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Auto Manufacturers',
        'current_price': 4850,
        'price_change_3y': -8.5,  # 3 TAHUN: TURUN dari ~5300
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
    },
    {
        'ticker': 'UNTR.JK',
        'name': 'United Tractors Tbk',
        'sector': 'Industrials',
        'industry': 'Farm & Heavy Machinery',
        'current_price': 29550,  # Update 25 Feb 2026: range 29300-29625, rilis laba 26 Feb
        'price_change_3y': 59.7,  # 3 TAHUN: dari ~18500 ke 29550
        'price_change_1y': 7.5,  # 1 TAHUN: 52w: 20025-32000, mcap Rp111.59T
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
    },
    {
        'ticker': 'AUTO.JK',
        'name': 'Astra Otoparts Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Auto Parts',
        'current_price': 2710,  # Update 23 Apr 2026
        'price_change_3y': 53.2,  # 3 TAHUN: dari ~1775 ke 2720
        'price_change_1y': 34.8,  # 1 TAHUN: +34.83% UPTREND!
        'debt_to_equity': 0.035,  # 3.5% - SANGAT RENDAH (update from web)
        'roe': 12.5,
        'roa': 7.8,
        'profit_margin': 8.2,
        'dividend_yield': 7.3,  # Update: 7.30%
        'current_ratio': 1.9,
        'earnings_growth': 15.2,
        'pe_ratio': 9.5,
        'pb_ratio': 1.2,
        'peg_ratio': 0.63,
        'market_cap': 10.5e12,
        'avg_volume': 1_500_000,
        'free_float_pct': 20,
    },

    # Retail
    {
        'ticker': 'ACES.JK',
        'name': 'Ace Hardware Indonesia',
        'sector': 'Consumer Cyclical',
        'industry': 'Home Improvement Retail',
        'current_price': 840,
        'price_change_3y': -15.2,  # 3 TAHUN: TURUN dari ~990
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
    },
    {
        'ticker': 'MAPI.JK',
        'name': 'Mitra Adiperkasa Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Apparel Retail',
        'current_price': 1650,
        'price_change_3y': 95.2,  # 3 TAHUN: dari ~845 - STRONG RECOVERY
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
        'market_cap': 71.84e12,  # Update from web
        'avg_volume': 12_000_000,
        'free_float_pct': 35,
        'notes': 'KOREKSI PARAH! -37.68% YoY, -12.38% bulanan',
    },

    # Properti
    {
        'ticker': 'BSDE.JK',
        'name': 'Bumi Serpong Damai Tbk',
        'sector': 'Real Estate',
        'industry': 'Real Estate Development',
        'current_price': 1150,
        'price_change_3y': 25.2,  # 3 TAHUN: recovery dari pandemi
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
    },
    {
        'ticker': 'CTRA.JK',
        'name': 'Ciputra Development Tbk',
        'sector': 'Real Estate',
        'industry': 'Real Estate Development',
        'current_price': 1180,
        'price_change_3y': 45.5,  # 3 TAHUN
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
    },

    # Semen
    {
        'ticker': 'SMGR.JK',
        'name': 'Semen Indonesia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 4250,
        'price_change_3y': -42.5,  # 3 TAHUN: TURUN SIGNIFIKAN dari ~7400
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
    },
    {
        'ticker': 'INTP.JK',
        'name': 'Indocement Tunggal Prakarsa',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 7500,
        'price_change_3y': -18.5,  # 3 TAHUN: TURUN dari ~9200
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
    },

    # Tower & Infrastruktur
    {
        'ticker': 'TOWR.JK',
        'name': 'Sarana Menara Nusantara',
        'sector': 'Real Estate',
        'industry': 'REIT - Specialty',
        'current_price': 885,
        'price_change_3y': -22.5,  # 3 TAHUN: TURUN dari ~1140
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
    },
    {
        'ticker': 'TBIG.JK',
        'name': 'Tower Bersama Infrastructure',
        'sector': 'Real Estate',
        'industry': 'REIT - Specialty',
        'current_price': 2150,
        'price_change_3y': -15.8,  # 3 TAHUN: TURUN dari ~2550
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
    },

    # Poultry/Peternakan
    {
        'ticker': 'CPIN.JK',
        'name': 'Charoen Pokphand Indonesia',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 5050,
        'price_change_3y': -5.8,  # 3 TAHUN: sedikit turun dari ~5360
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
    },
    {
        'ticker': 'JPFA.JK',
        'name': 'Japfa Comfeed Indonesia',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 1580,
        'price_change_3y': 58.2,  # 3 TAHUN: dari ~998
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
    },

    # Media
    {
        'ticker': 'SCMA.JK',
        'name': 'Surya Citra Media Tbk',
        'sector': 'Communication Services',
        'industry': 'Broadcasting',
        'current_price': 142,
        'price_change_3y': -68.5,  # 3 TAHUN: TURUN SANGAT SIGNIFIKAN dari ~450
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
    },

    # Keramik
    {
        'ticker': 'ARNA.JK',
        'name': 'Arwana Citramulia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Building Materials',
        'current_price': 595,
        'price_change_3y': 38.5,  # 3 TAHUN: dari ~430
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
    },

    # Elektronik Retail
    {
        'ticker': 'ERAA.JK',
        'name': 'Erajaya Swasembada Tbk',
        'sector': 'Consumer Cyclical',
        'industry': 'Electronics & Appliances',
        'current_price': 428,
        'price_change_3y': 72.5,  # 3 TAHUN: dari ~248
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
    },

    # =========================================================================
    # SAHAM BARU - Verified passing all 5 criteria (April 2026)
    # =========================================================================

    # Tin Mining - VERIFIED PASS
    {
        'ticker': 'TINS.JK',
        'name': 'Timah Tbk',
        'sector': 'Basic Materials',
        'industry': 'Tin Mining',
        'current_price': 3940,  # Update 23 Apr 2026: +7.65%
        'price_change_3y': 370.3,  # 3 TAHUN: dari ~825 ke 3880
        'price_change_1y': 255.8,  # 1 TAHUN: EXPLOSIVE dari ~1090
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
        'free_float_pct': 35,
        'notes': 'TIN MINING - RKAB export recovery 2026, profit +176% YoY',
    },

    # Palm Oil Plantation - VERIFIED PASS
    {
        'ticker': 'AALI.JK',
        'name': 'Astra Agro Lestari Tbk',
        'sector': 'Consumer Defensive',
        'industry': 'Farm Products',
        'current_price': 7350,  # Update 17 Apr 2026
        'price_change_3y': 41.3,  # 3 TAHUN: dari ~5200 ke 7350
        'price_change_1y': 28.4,  # 1 TAHUN: +28.38%
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
        'free_float_pct': 20,
        'notes': 'CPO plantation - low debt, consistent dividend',
    },

    # Pharmaceutical - VERIFIED PASS
    {
        'ticker': 'TSPC.JK',
        'name': 'Tempo Scan Pacific Tbk',
        'sector': 'Healthcare',
        'industry': 'Drug Manufacturers',
        'current_price': 2430,  # Update 17 Apr 2026
        'price_change_3y': 35.6,  # 3 TAHUN: dari ~1790 ke 2430
        'price_change_1y': 18.7,  # 1 TAHUN: +18.67%
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
        'free_float_pct': 25,
        'notes': 'Pharma defensive - consistent growth, low debt',
    },
]
