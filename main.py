#!/usr/bin/env python3
"""
==============================================================================
    IHSG STOCK ANALYZER - ALA WARREN BUFFETT
==============================================================================

Aplikasi untuk menganalisis saham-saham di IHSG (Bursa Efek Indonesia)
menggunakan prinsip-prinsip investasi Warren Buffett.

Kriteria yang digunakan:
1. Trend harga 3 tahun naik (lebih reliable)
2. Hutang rendah (D/E ratio)
3. Profitabilitas tinggi (ROE, Profit Margin)
4. Membayar dividen
5. Likuiditas baik (Current Ratio)

Author: Warren Buffett Style Analyzer
"""

import pandas as pd
import numpy as np
from datetime import datetime
from tabulate import tabulate
import sys

from config import IHSG_STOCKS, SCORING_WEIGHTS
from data_fetcher import StockDataFetcher, format_number
from buffett_scorer import BuffettScorer, explain_buffett_formula


def print_header():
    """Print header aplikasi"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ██╗██╗  ██╗███████╗ ██████╗     ███████╗████████╗ ██████╗  ██████╗██╗  ██╗║
║     ██║██║  ██║██╔════╝██╔════╝     ██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝║
║     ██║███████║███████╗██║  ███╗    ███████╗   ██║   ██║   ██║██║     █████╔╝ ║
║     ██║██╔══██║╚════██║██║   ██║    ╚════██║   ██║   ██║   ██║██║     ██╔═██╗ ║
║     ██║██║  ██║███████║╚██████╔╝    ███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗║
║     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝     ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝║
║                                                                              ║
║              ANALYZER - WARREN BUFFETT STYLE                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   "Price is what you pay. Value is what you get." - Warren Buffett          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def print_criteria():
    """Print kriteria yang digunakan"""
    print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                         KRITERIA SELEKSI SAHAM                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ✓ Trend Harga 3 TAHUN: NAIK (positif) - lebih reliable                    │
│   ✓ Hutang Rendah: D/E Ratio < 1.0                                          │
│   ✓ Profitabilitas: ROE > 15%, Profit Margin > 10%                          │
│   ✓ Dividen: Membayar dividen (yield > 1%)                                  │
│   ✓ Likuiditas: Current Ratio > 1.0                                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
    """)


def print_weights():
    """Print bobot scoring"""
    print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                           BOBOT SCORING                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   • Debt to Equity (Hutang)    : 20%  ← Rendah lebih baik                   │
│   • Return on Equity (ROE)     : 20%  ← Tinggi lebih baik                   │
│   • Trend Harga 3 TAHUN        : 15%  ← Positif dan tinggi lebih baik       │
│   • Profit Margin              : 15%  ← Tinggi lebih baik                   │
│   • Dividend Yield             : 15%  ← Tinggi lebih baik                   │
│   • Current Ratio (Likuiditas) : 10%  ← Di atas 1.0 lebih baik              │
│   • Earnings Growth            : 5%   ← Positif lebih baik                  │
│                                                                              │
│   TOTAL                        : 100%                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
    """)


def display_top_stocks(ranked_df: pd.DataFrame, top_n: int = 10):
    """
    Tampilkan hasil ranking saham top N
    """
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  🏆 TOP {top_n} SAHAM IHSG ALA WARREN BUFFETT 🏆                ║
╠══════════════════════════════════════════════════════════════════════════════╣
    """)

    # Siapkan data untuk tabel
    table_data = []
    for _, row in ranked_df.iterrows():
        table_data.append([
            int(row['rank']),
            row['ticker'].replace('.JK', ''),
            row['name'][:25] if pd.notna(row['name']) else 'N/A',
            format_number(row['price_change_1y'], 1, '%'),
            format_number(row['debt_to_equity'], 2),
            format_number(row['roe'], 1, '%'),
            format_number(row['profit_margin'], 1, '%'),
            format_number(row['dividend_yield'], 1, '%'),
            format_number(row['buffett_score'], 1),
        ])

    headers = ['Rank', 'Ticker', 'Nama', 'Return 1Y', 'D/E', 'ROE', 'Margin', 'Div Yld', 'Score']

    print(tabulate(table_data, headers=headers, tablefmt='grid', numalign='right'))
    print()


def display_detailed_analysis(ranked_df: pd.DataFrame):
    """
    Tampilkan analisis detail untuk setiap saham
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ANALISIS DETAIL PER SAHAM                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    for _, row in ranked_df.iterrows():
        ticker = row['ticker'].replace('.JK', '')

        # Evaluasi untuk tiap metrik
        de_status = '✓ BAIK' if pd.notna(row['debt_to_equity']) and row['debt_to_equity'] < 1 else '⚠ TINGGI'
        roe_status = '✓ SANGAT BAIK' if pd.notna(row['roe']) and row['roe'] > 15 else '⚠ PERLU DITINGKATKAN'
        div_status = '✓ MEMBAYAR DIVIDEN' if pd.notna(row['dividend_yield']) and row['dividend_yield'] > 0 else '⚠ TIDAK ADA'

        print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│  #{int(row['rank'])} - {ticker} - {str(row['name'])[:50] if pd.notna(row['name']) else 'N/A'}
├──────────────────────────────────────────────────────────────────────────────┤
│
│  📈 HARGA & TREND
│     • Harga Saat Ini   : Rp {format_number(row['current_price'], 0)}
│     • Return 1 Tahun   : {format_number(row['price_change_1y'], 2, '%')}
│
│  💰 HUTANG (DEBT)
│     • Debt/Equity      : {format_number(row['debt_to_equity'], 2)}
│     → {de_status}
│
│  📊 PROFITABILITAS
│     • ROE              : {format_number(row['roe'], 2, '%')}
│     • Profit Margin    : {format_number(row['profit_margin'], 2, '%')}
│     → {roe_status}
│
│  💵 DIVIDEN
│     • Dividend Yield   : {format_number(row['dividend_yield'], 2, '%')}
│     → {div_status}
│
│  🏦 VALUASI
│     • P/E Ratio        : {format_number(row.get('pe_ratio'), 2)}
│     • P/B Ratio        : {format_number(row.get('pb_ratio'), 2)}
│     • Market Cap       : Rp {format_number(row.get('market_cap'), 1, 'T')}
│
│  ⭐ BUFFETT SCORE      : {format_number(row['buffett_score'], 1)} / 100
│
└──────────────────────────────────────────────────────────────────────────────┘
        """)


def display_score_breakdown(ranked_df: pd.DataFrame):
    """
    Tampilkan breakdown skor untuk setiap komponen
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       BREAKDOWN SKOR PER KOMPONEN                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Siapkan data untuk tabel
    score_cols = ['score_price_trend', 'score_debt', 'score_roe',
                  'score_margin', 'score_dividend', 'score_liquidity', 'score_growth']

    table_data = []
    for _, row in ranked_df.iterrows():
        row_data = [
            int(row['rank']),
            row['ticker'].replace('.JK', ''),
        ]
        for col in score_cols:
            if col in row:
                row_data.append(format_number(row[col], 0))
            else:
                row_data.append('N/A')
        row_data.append(format_number(row['buffett_score'], 1))
        table_data.append(row_data)

    headers = ['#', 'Ticker', 'Trend', 'Debt', 'ROE', 'Margin', 'Div', 'Liq', 'Growth', 'TOTAL']
    print(tabulate(table_data, headers=headers, tablefmt='grid', numalign='right'))

    print("""
    Keterangan Skor (0-100):
    ┌────────────────────────────────────────────────────────────┐
    │ Trend  : Skor trend harga 1 tahun (tinggi = lebih baik)   │
    │ Debt   : Skor hutang/D/E ratio (rendah = lebih baik)      │
    │ ROE    : Skor Return on Equity (tinggi = lebih baik)      │
    │ Margin : Skor Profit Margin (tinggi = lebih baik)         │
    │ Div    : Skor Dividend Yield (tinggi = lebih baik)        │
    │ Liq    : Skor Current Ratio (tinggi = lebih baik)         │
    │ Growth : Skor Earnings Growth (tinggi = lebih baik)       │
    │ TOTAL  : Buffett Score (weighted average)                 │
    └────────────────────────────────────────────────────────────┘
    """)


def display_investment_recommendation(ranked_df: pd.DataFrame):
    """
    Tampilkan rekomendasi investasi berdasarkan analisis
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       REKOMENDASI INVESTASI                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Kategori berdasarkan skor
    top_3 = ranked_df.head(3)
    mid = ranked_df.iloc[3:7] if len(ranked_df) > 3 else pd.DataFrame()
    lower = ranked_df.iloc[7:10] if len(ranked_df) > 7 else pd.DataFrame()

    print("""
    🥇 KATEGORI A - SANGAT DIREKOMENDASIKAN (Top 3)
    ════════════════════════════════════════════════════════════
    """)
    for _, row in top_3.iterrows():
        ticker = row['ticker'].replace('.JK', '')
        print(f"       #{int(row['rank'])}. {ticker:6} │ Score: {row['buffett_score']:.1f} │ {str(row['name'])[:30] if pd.notna(row['name']) else ''}")

    if not mid.empty:
        print("""
    🥈 KATEGORI B - DIREKOMENDASIKAN (Rank 4-7)
    ════════════════════════════════════════════════════════════
        """)
        for _, row in mid.iterrows():
            ticker = row['ticker'].replace('.JK', '')
            print(f"       #{int(row['rank'])}. {ticker:6} │ Score: {row['buffett_score']:.1f} │ {str(row['name'])[:30] if pd.notna(row['name']) else ''}")

    if not lower.empty:
        print("""
    🥉 KATEGORI C - LAYAK DIPERTIMBANGKAN (Rank 8-10)
    ════════════════════════════════════════════════════════════
        """)
        for _, row in lower.iterrows():
            ticker = row['ticker'].replace('.JK', '')
            print(f"       #{int(row['rank'])}. {ticker:6} │ Score: {row['buffett_score']:.1f} │ {str(row['name'])[:30] if pd.notna(row['name']) else ''}")


def display_formula_summary():
    """
    Tampilkan ringkasan formula scoring
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RINGKASAN FORMULA BUFFETT SCORE                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   BUFFETT SCORE = (0.20 × Debt Score) + (0.20 × ROE Score) +                ║
║                   (0.15 × Trend Score) + (0.15 × Margin Score) +            ║
║                   (0.15 × Dividend Score) + (0.10 × Liquidity Score) +      ║
║                   (0.05 × Growth Score)                                     ║
║                                                                              ║
║   Dimana setiap komponen dinormalisasi ke skala 0-100                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def save_results(ranked_df: pd.DataFrame, all_data_df: pd.DataFrame):
    """
    Simpan hasil analisis ke file CSV
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Simpan top 10
    top10_file = f'results_top10_{timestamp}.csv'
    ranked_df.to_csv(top10_file, index=False)

    # Simpan semua data
    all_file = f'results_all_{timestamp}.csv'
    all_data_df.to_csv(all_file, index=False)

    print(f"""
    💾 Hasil disimpan ke:
       • {top10_file}
       • {all_file}
    """)

    return top10_file, all_file


def try_fetch_live_data():
    """
    Coba ambil data live dari Yahoo Finance
    Returns DataFrame atau None jika gagal
    """
    fetcher = StockDataFetcher()

    print("\n" + "="*60)
    print("  MENCOBA MENGAMBIL DATA LIVE DARI YAHOO FINANCE...")
    print("="*60)

    # Coba ambil satu saham dulu untuk test koneksi
    test_data = fetcher.get_stock_data("BBCA.JK")

    if test_data:
        print("  ✓ Koneksi berhasil! Mengambil semua data...")
        return fetcher.fetch_all_stocks(IHSG_STOCKS)
    else:
        print("  ✗ Tidak dapat terhubung ke Yahoo Finance")
        return None


def load_sample_data():
    """
    Load sample data untuk demonstrasi
    """
    from sample_data import SAMPLE_STOCK_DATA

    print("\n" + "="*60)
    print("  MENGGUNAKAN SAMPLE DATA UNTUK DEMONSTRASI")
    print("="*60)
    print("  (Data berdasarkan informasi publik Q4 2024/Q1 2025)")

    df = pd.DataFrame(SAMPLE_STOCK_DATA)
    print(f"\n  Total saham dalam sample: {len(df)}")

    return df


def main():
    """
    Fungsi utama untuk menjalankan analisis
    """
    print_header()
    print_criteria()
    print_weights()

    # Tampilkan formula
    print(explain_buffett_formula())

    # Coba ambil data live, jika gagal gunakan sample
    df = try_fetch_live_data()

    if df is None or df.empty:
        df = load_sample_data()

    if df.empty:
        print("\n[ERROR] Tidak ada data saham yang tersedia!")
        return

    # Inisialisasi scorer
    scorer = BuffettScorer(SCORING_WEIGHTS)

    # Hitung skor dan ranking
    print("\n" + "="*60)
    print("  MENGHITUNG SKOR DAN RANKING...")
    print("="*60)

    ranked = scorer.get_ranking(df, top_n=10)

    if ranked.empty:
        print("\n[ERROR] Tidak ada saham yang memenuhi kriteria!")
        return

    # Tampilkan hasil
    display_formula_summary()
    display_top_stocks(ranked)
    display_score_breakdown(ranked)
    display_detailed_analysis(ranked)
    display_investment_recommendation(ranked)

    # Simpan hasil
    top10_file, all_file = save_results(ranked, df)

    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              DISCLAIMER                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Analisis ini dibuat untuk tujuan EDUKASI dan REFERENSI semata.             ║
║  BUKAN merupakan rekomendasi untuk membeli atau menjual saham.              ║
║                                                                              ║
║  Investasi saham memiliki RISIKO. Selalu lakukan riset mandiri (DYOR)       ║
║  sebelum mengambil keputusan investasi.                                     ║
║                                                                              ║
║  "Risk comes from not knowing what you're doing." - Warren Buffett          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    return ranked


if __name__ == "__main__":
    result = main()
