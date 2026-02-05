"""
Konfigurasi untuk Analisis Saham IHSG ala Warren Buffett
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

# Bobot untuk sistem scoring Warren Buffett
SCORING_WEIGHTS = {
    'price_trend_1y': 0.15,      # Trend harga 1 tahun (15%)
    'debt_to_equity': 0.20,      # Rasio hutang (20%) - semakin rendah semakin baik
    'roe': 0.20,                 # Return on Equity (20%)
    'profit_margin': 0.15,       # Profit Margin (15%)
    'dividend_yield': 0.15,      # Dividend Yield (15%)
    'current_ratio': 0.10,       # Current Ratio (10%)
    'earnings_growth': 0.05,     # Pertumbuhan Laba (5%)
}

# Kriteria minimum Warren Buffett
MIN_CRITERIA = {
    'min_roe': 15,              # ROE minimal 15%
    'max_debt_to_equity': 1.0,  # D/E ratio maksimal 1.0
    'min_profit_margin': 10,    # Profit margin minimal 10%
    'min_dividend_yield': 1.0,  # Dividend yield minimal 1%
    'min_current_ratio': 1.0,   # Current ratio minimal 1.0
}
