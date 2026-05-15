"""
Konfigurasi untuk Analisis Saham IHSG ala Warren Buffett
Version 2.0 - Dengan Valuation Score dan Liquidity Filter
"""

# Daftar saham-saham IHSG yang akan dianalisis
# Format: Ticker Yahoo Finance untuk saham Indonesia adalah KODE.JK
IHSG_STOCKS = [
    # Perbankan
    "BBCA.JK",  # Bank Central Asia
    "BBRI.JK",  # Bank Rakyat Indonesia
    "BMRI.JK",  # Bank Mandiri
    "BBNI.JK",  # Bank Negara Indonesia
    "BRIS.JK",  # Bank Syariah Indonesia

    # Consumer Goods
    "UNVR.JK",  # Unilever Indonesia
    "ICBP.JK",  # Indofood CBP
    "INDF.JK",  # Indofood Sukses Makmur
    "MYOR.JK",  # Mayora Indah
    "KLBF.JK",  # Kalbe Farma
    "SIDO.JK",  # Sido Muncul
    "CPIN.JK",  # Charoen Pokphand

    # Telekomunikasi
    "TLKM.JK",  # Telkom Indonesia
    "EXCL.JK",  # XL Axiata
    "ISAT.JK",  # Indosat Ooredoo

    # Semen & Konstruksi
    "SMGR.JK",  # Semen Indonesia
    "INTP.JK",  # Indocement
    "WIKA.JK",  # Wijaya Karya
    "PTPP.JK",  # PP Persero

    # Mining & Energy
    "ADRO.JK",  # Adaro Energy
    "ITMG.JK",  # Indo Tambangraya
    "PTBA.JK",  # Bukit Asam
    "MEDC.JK",  # Medco Energi
    "INCO.JK",  # Vale Indonesia
    "ANTM.JK",  # Aneka Tambang

    # Properti & Real Estate
    "BSDE.JK",  # Bumi Serpong Damai
    "CTRA.JK",  # Ciputra Development
    "SMRA.JK",  # Summarecon

    # Otomotif
    "ASII.JK",  # Astra International
    "AUTO.JK",  # Astra Otoparts

    # Retail
    "ACES.JK",  # Ace Hardware
    "MAPI.JK",  # Mitra Adiperkasa
    "LPPF.JK",  # Matahari Department Store
    "AMRT.JK",  # Alfamart (Sumber Alfaria)

    # Healthcare
    "HEAL.JK",  # Medikaloka Hermina

    # Industri
    "SRIL.JK",  # Sri Rejeki Isman
    "GGRM.JK",  # Gudang Garam
    "HMSP.JK",  # HM Sampoerna

    # Finance Non-Bank
    "BDMN.JK",  # Bank Danamon
    "BTPS.JK",  # Bank BTPN Syariah
    "PNBN.JK",  # Panin Bank

    # Teknologi & Media
    "EMTK.JK",  # Elang Mahkota
    "SCMA.JK",  # Surya Citra Media

    # Lainnya
    "UNTR.JK",  # United Tractors
    "SMDR.JK",  # Samudera Indonesia
    "JPFA.JK",  # Japfa Comfeed
    "ERAA.JK",  # Erajaya Swasembada
    "ARNA.JK",  # Arwana Citramulia
    "TOWR.JK",  # Sarana Menara Nusantara
    "TBIG.JK",  # Tower Bersama
]

# ============================================================================
# FORMULA BUFFETT SCORE V2.0
# ============================================================================
# Menambahkan Valuation Score dengan bobot signifikan
# Rekomendasi: Valuasi 25-30% (bukan 40%) karena DCF sensitif terhadap asumsi
#
# Formula:
# BUFFETT_SCORE = (0.15 × Debt) + (0.15 × ROE) + (0.10 × Trend) +
#                 (0.10 × Margin) + (0.10 × Dividend) + (0.10 × Liquidity) +
#                 (0.05 × Growth) + (0.25 × Valuation)
# ============================================================================

SCORING_WEIGHTS = {
    'debt_to_equity': 0.15,      # Rasio hutang (15%) - rendah lebih baik
    'roe': 0.15,                 # Return on Equity (15%)
    'price_trend_3y': 0.10,      # Trend harga 3 TAHUN (10%) - Changed from 1y to 3y
    'profit_margin': 0.10,       # Profit Margin (10%)
    'dividend_yield': 0.10,      # Dividend Yield (10%)
    'current_ratio': 0.05,       # Current Ratio (5%)
    'earnings_growth': 0.05,     # Pertumbuhan Laba (5%)
    'valuation': 0.25,           # Valuation Score - PEG, P/E, P/B (25%)
    'liquidity': 0.05,           # Trading Liquidity/Volume (5%)
}

# ============================================================================
# KRITERIA MINIMUM V5.0 - POST MSCI
# ============================================================================
# Update setelah kasus MSCI menghapus 6 saham Indonesia karena:
# - Transparansi rendah
# - Free float rendah
# - Konsentrasi kepemilikan tinggi
# ============================================================================

MIN_CRITERIA = {
    'min_roe': 10,              # ROE minimal 10% (naik dari >0%)
    'max_debt_to_equity': 0.5,  # D/E ratio maksimal 50% untuk non-bank
    'min_profit_margin': 5,     # Profit margin minimal 5%
    'min_dividend_yield': 0,    # Dividend yield minimal > 0%
    'max_payout_ratio': 80,     # Payout ratio maksimal 80% (sustainable)
    'min_current_ratio': 1.0,   # Current ratio minimal 1.0
    'max_per': 20,              # P/E ratio maksimal 20x
    'max_pbv': 3.0,             # P/B ratio maksimal 3x
}

# ============================================================================
# GOVERNANCE CRITERIA V5.0 - Anti MSCI Risk
# ============================================================================
# Filter baru untuk menghindari saham yang bisa di-kick dari indeks global
# ============================================================================

GOVERNANCE_CRITERIA = {
    'min_free_float_pct': 15,           # Minimal 15% free float (aturan baru BEI)
    'max_ownership_concentration': 80,   # Maksimal 80% kepemilikan terkonsentrasi
    'require_positive_ocf': True,        # Operating Cash Flow harus positif
    'governance_flags': [                # Red flags yang harus dihindari
        'transparency_issue',
        'ownership_concentration',
        'index_removal_risk',
        'related_party_transaction',
        'audit_concern',
    ]
}

# ============================================================================
# LIQUIDITY FILTER - Anti Goreng
# ============================================================================
# Saham dengan volume rendah mudah dimanipulasi (digoreng)
# Filter:
# 1. Average Daily Volume minimal 1 juta lembar
# 2. Market Cap minimal 5 Triliun Rupiah
# 3. Free Float minimal 15%
# ============================================================================

LIQUIDITY_CRITERIA = {
    'min_avg_volume': 1_000_000,      # Minimal 1 juta lembar per hari
    'min_market_cap': 5e12,           # Minimal 5 Triliun Rupiah
    'min_free_float_pct': 15,         # Minimal 15% free float
}

# ============================================================================
# VALUATION CRITERIA
# ============================================================================
# Untuk menilai apakah saham undervalued atau overvalued
# Menggunakan kombinasi:
# 1. PEG Ratio (P/E dibagi Growth) - ideal < 1
# 2. P/E Ratio relatif terhadap industri
# 3. P/B Ratio - ideal < 2 untuk value investing
# ============================================================================

VALUATION_BENCHMARKS = {
    'ideal_peg': 1.0,           # PEG < 1 = undervalued
    'max_pe_ratio': 20,         # P/E > 20 mulai mahal
    'ideal_pb_ratio': 2.0,      # P/B < 2 untuk value
    'sector_pe': {              # P/E rata-rata per sektor
        'Financial Services': 12,
        'Energy': 8,
        'Basic Materials': 10,
        'Consumer Defensive': 18,
        'Consumer Cyclical': 15,
        'Healthcare': 20,
        'Communication Services': 12,
        'Real Estate': 15,
        'Industrials': 12,
    }
}
