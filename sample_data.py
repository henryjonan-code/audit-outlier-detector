"""
Sample Data Saham IHSG untuk Demonstrasi
Version 2.2 - Dengan Return 3 Tahun, Volume dan Valuasi Data

============================================================================
DISCLAIMER PENTING:
============================================================================
Data ini HANYA ESTIMASI untuk demonstrasi sistem scoring.
Data TIDAK REAL-TIME dan mungkin TIDAK AKURAT.

SEBELUM membuat keputusan investasi:
1. Verifikasi harga terkini di platform trading resmi (Stockbit, RTI, IDX)
2. Periksa laporan keuangan di IDX atau situs resmi emiten
3. Konsultasi dengan analis atau financial advisor

Sistem ini adalah ALAT BANTU screening, BUKAN rekomendasi investasi.
============================================================================
"""

SAMPLE_STOCK_DATA = [
    # Bank - Perbankan (High Liquidity)
    {
        'ticker': 'BBCA.JK',
        'name': 'Bank Central Asia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks - Regional',
        'current_price': 9875,
        'price_change_3y': 45.2,  # 3 TAHUN: dari ~6800 ke 9875
        'price_change_1y': 12.5,  # 1 TAHUN: steady uptrend
        'debt_to_equity': 0.82,
        'roe': 21.5,
        'roa': 3.8,
        'profit_margin': 45.2,
        'dividend_yield': 2.8,
        'current_ratio': None,
        'earnings_growth': 15.3,
        'pe_ratio': 22.5,
        'pb_ratio': 4.8,
        'peg_ratio': 1.47,
        'market_cap': 1250e12,
        'avg_volume': 25_000_000,
        'free_float_pct': 45,
    },
    {
        'ticker': 'BBRI.JK',
        'name': 'Bank Rakyat Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks - Regional',
        'current_price': 4650,
        'price_change_3y': 28.5,  # 3 TAHUN: dari ~3600 ke 4650
        'debt_to_equity': 0.95,
        'roe': 19.8,
        'roa': 3.2,
        'profit_margin': 35.8,
        'dividend_yield': 5.2,
        'current_ratio': None,
        'earnings_growth': 12.1,
        'pe_ratio': 12.8,
        'pb_ratio': 2.5,
        'peg_ratio': 1.06,
        'market_cap': 720e12,
        'avg_volume': 80_000_000,
        'free_float_pct': 43,
    },
    {
        'ticker': 'BMRI.JK',
        'name': 'Bank Mandiri Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks - Regional',
        'current_price': 6200,
        'price_change_3y': 55.8,  # 3 TAHUN: dari ~3980 ke 6200 - STRONG PERFORMER
        'price_change_1y': 18.5,  # 1 TAHUN: strong uptrend
        'debt_to_equity': 0.88,
        'roe': 22.3,
        'roa': 3.5,
        'profit_margin': 38.5,
        'dividend_yield': 4.8,
        'current_ratio': None,
        'earnings_growth': 18.5,
        'pe_ratio': 10.2,
        'pb_ratio': 2.3,
        'peg_ratio': 0.55,
        'market_cap': 580e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 40,
    },
    {
        'ticker': 'BBNI.JK',
        'name': 'Bank Negara Indonesia Tbk',
        'sector': 'Financial Services',
        'industry': 'Banks - Regional',
        'current_price': 4850,
        'price_change_3y': 18.5,  # 3 TAHUN: lebih lambat dari peers
        'debt_to_equity': 0.92,
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
    },

    # Consumer Goods
    {
        'ticker': 'ICBP.JK',
        'name': 'Indofood CBP Sukses Makmur',
        'sector': 'Consumer Defensive',
        'industry': 'Packaged Foods',
        'current_price': 11500,
        'price_change_3y': 52.8,  # 3 TAHUN: dari ~7530 ke 11500
        'price_change_1y': 22.5,  # 1 TAHUN: strong uptrend - consumer staple winner
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
        'current_price': 2450,
        'price_change_3y': 68.5,  # 3 TAHUN: STRONG PERFORMER
        'price_change_1y': 28.5,  # 1 TAHUN: STRONG - ekspor Asia kuat
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
        'market_cap': 55e12,
        'avg_volume': 3_500_000,
        'free_float_pct': 67,
    },

    # Telekomunikasi
    {
        'ticker': 'TLKM.JK',
        'name': 'Telkom Indonesia Tbk',
        'sector': 'Communication Services',
        'industry': 'Telecom Services',
        'current_price': 2850,
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
        'current_price': 22125,  # FIXED: Harga aktual Feb 2025
        'price_change_3y': 85.5,   # 3 TAHUN: dari ~12000 (Feb 2022) - sudah KOREKSI dari peak 45000
        'price_change_1y': -11.5,  # 1 TAHUN: TURUN dari ~25000 ke 22125 - DOWNTREND!
        'debt_to_equity': 0.25,
        'roe': 35.2,  # Sudah turun dari puncak karena coal price turun
        'roa': 22.5,
        'profit_margin': 18.5,  # Margin menyusut karena coal price normalisasi
        'dividend_yield': 10.5,  # Masih tinggi tapi turun dari peak 15%+
        'current_ratio': 3.2,
        'earnings_growth': -15.8,  # NEGATIF: Earnings TURUN YoY karena coal price turun
        'pe_ratio': 5.5,
        'pb_ratio': 1.8,
        'peg_ratio': None,  # Negative growth = no PEG
        'market_cap': 25e12,
        'avg_volume': 2_500_000,
        'free_float_pct': 35,
        'notes': 'Coal cycle sudah peak, earnings declining YoY',
    },
    {
        'ticker': 'PTBA.JK',
        'name': 'Bukit Asam Tbk',
        'sector': 'Energy',
        'industry': 'Thermal Coal',
        'current_price': 2650,  # FIXED: Harga aktual Feb 2025
        'price_change_3y': 65.5,  # 3 TAHUN: dari ~1600 - masih positif
        'price_change_1y': -22.5,  # 1 TAHUN: TURUN signifikan - DOWNTREND!
        'debt_to_equity': 0.28,
        'roe': 28.5,  # Turun dari peak
        'roa': 16.5,
        'profit_margin': 20.5,  # Margin menyusut
        'dividend_yield': 8.5,
        'current_ratio': 2.5,
        'earnings_growth': -18.5,  # NEGATIF: Earnings turun YoY
        'pe_ratio': 6.5,
        'pb_ratio': 1.8,
        'peg_ratio': None,  # Negative growth
        'market_cap': 30e12,
        'avg_volume': 15_000_000,
        'free_float_pct': 35,
        'notes': 'Coal cycle sudah peak, DMO policy pressure',
    },
    {
        'ticker': 'INCO.JK',
        'name': 'Vale Indonesia Tbk',
        'sector': 'Basic Materials',
        'industry': 'Nickel',
        'current_price': 3850,  # FIXED: Harga turun karena nickel price pressure
        'price_change_3y': 105.5,  # 3 TAHUN: dari ~1885 - masih positif
        'price_change_1y': -15.5,  # 1 TAHUN: TURUN karena nickel oversupply
        'debt_to_equity': 0.15,
        'roe': 12.5,  # Turun dari peak
        'roa': 8.8,
        'profit_margin': 15.5,  # Margin menyusut karena nickel price turun
        'dividend_yield': 3.2,
        'current_ratio': 4.5,
        'earnings_growth': -25.2,  # NEGATIF: Nickel glut impact
        'pe_ratio': 15.5,
        'pb_ratio': 1.9,
        'peg_ratio': None,  # Negative growth
        'market_cap': 38e12,
        'avg_volume': 18_000_000,
        'free_float_pct': 21,
        'notes': 'Nickel oversupply dari China/Indonesia menekan harga',
    },
    {
        'ticker': 'ANTM.JK',
        'name': 'Aneka Tambang Tbk',
        'sector': 'Basic Materials',
        'industry': 'Other Industrial Metals',
        'current_price': 1850,
        'price_change_3y': 85.5,  # 3 TAHUN: dari ~998
        'debt_to_equity': 0.42,
        'roe': 15.8,
        'roa': 8.5,
        'profit_margin': 12.5,
        'dividend_yield': 3.8,
        'current_ratio': 2.2,
        'earnings_growth': 32.5,
        'pe_ratio': 10.2,
        'pb_ratio': 1.6,
        'peg_ratio': 0.31,
        'market_cap': 45e12,
        'avg_volume': 45_000_000,
        'free_float_pct': 35,
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
        'current_price': 27500,
        'price_change_3y': 48.5,  # 3 TAHUN: dari ~18500
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
        'current_price': 2180,
        'price_change_3y': 32.5,  # 3 TAHUN
        'debt_to_equity': 0.32,
        'roe': 12.5,
        'roa': 7.8,
        'profit_margin': 8.2,
        'dividend_yield': 4.2,
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
        'current_price': 2850,
        'price_change_3y': 112.5,  # 3 TAHUN: dari ~1340 - STRONG PERFORMER
        'price_change_1y': 35.5,   # 1 TAHUN: STRONG UPTREND - ekspansi agresif
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
        'market_cap': 115e12,
        'avg_volume': 12_000_000,
        'free_float_pct': 35,
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
]
