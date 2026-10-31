"""
HSC Blacklist - Saham High Shareholding Concentration
=====================================================
Saham yang DIKELUARKAN BEI dari perhitungan IHSG (dan IDX30, LQ45, IDX80).

Dasar: Pengumuman BEI Peng-00201/BEI.POP/10-2026 (21 Okt 2026)
Efektif: 2 November 2026
Status: BUKAN delisting - saham tetap bisa diperdagangkan,
        tapi pergerakan harganya tidak lagi dihitung di indeks utama.

ALASAN: Free float terlalu kecil / kepemilikan terkonsentrasi (HSC).
        Rawan dimanipulasi. Secara prinsip Buffett = governance/likuiditas
        buruk, jadi WAJIB dikeluarkan dari radar screener kita.

CARA UPDATE:
  - Daftar ini DINAMIS. BEI bisa menamb/mengurangi tiap evaluasi.
  - Jadwal evaluasi: Jan, Apr, Jul, Okt (efektif hari bursa pertama
    Feb, Mei, Agu, Nov). Perubahan di luar jadwal juga langsung berlaku.
  - Kalau ada pengumuman baru, tambahkan/hapus ticker di set di bawah
    dan update LAST_UPDATED + jumlahnya.

Sumber verifikasi: idx.co.id (pengumuman resmi), detikFinance, Kontan, Bisnis.
"""

LAST_UPDATED = "27 Oktober 2026"
EFFECTIVE_DATE = "2 November 2026"
ANNOUNCEMENT = "Peng-00201/BEI.POP/10-2026"

# =============================================================================
# DAFTAR HITAM HSC (per 27 Okt 2026 - total 82 emiten)
# Catatan: 2 ticker dari screenshot awal tertutup ikon (kemungkinan SHIP + 1),
#          diverifikasi dari pemberitaan detikFinance/Kontan/Bisnis.
# =============================================================================
HSC_BLACKLIST = {
    # Batch awal 80 (efektif 2 Nov 2026)
    "MPRO", "DCII", "BBSI", "PGUN", "POLU", "SOHO", "BNLI", "YUPI",
    "ROCK", "PRAY", "BTPN", "FAPA", "IFSH", "SMAR", "MLPT", "CMNT",
    "GEMS", "LIFE", "BNII", "ELPI", "MCOL", "BYAN", "KING", "SOTS",
    "DNET", "RISE", "AGII", "ALII", "DGWG", "BREN", "SRAJ", "MKPI",
    "SILO", "HATM", "TBIG", "WBSA", "DSSA", "MEGA", "MORA", "RLCO",
    "KONI", "FITT", "STTP", "BINA", "SATU", "TCPI", "BELI", "MGRO",
    "SSMS", "BBHI", "CMNP", "AGAR", "ALKA", "BKDP", "BAJA", "MDIA",
    "BDKR", "SAFE", "NICK", "MSJA", "BIKE", "INDO", "BSWD", "PSAB",
    "SMMT", "CITA", "BMAS", "MTEL", "ADES", "SAME", "BBMD", "SHIP",
    "INPP", "EPMT", "DUTI", "MAYA", "CLAY", "TMAS", "DMND",
    # Tambahan per 27 Okt 2026 (jadi 82)
    "TFCO", "FILM",
}


def normalize(ticker: str) -> str:
    """Buang suffix .JK dan rapikan jadi uppercase."""
    return str(ticker).replace(".JK", "").strip().upper()


def is_hsc(ticker: str) -> bool:
    """True jika saham masuk daftar hitam HSC (harus dikeluarkan dari radar)."""
    return normalize(ticker) in HSC_BLACKLIST


if __name__ == "__main__":
    print(f"HSC Blacklist - update {LAST_UPDATED}")
    print(f"Efektif {EFFECTIVE_DATE} | {ANNOUNCEMENT}")
    print(f"Total: {len(HSC_BLACKLIST)} emiten")
