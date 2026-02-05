"""
Sistem Scoring Saham ala Warren Buffett

Prinsip-prinsip Warren Buffett yang digunakan:
1. Cari perusahaan dengan competitive advantage (moat)
2. Hutang rendah - perusahaan yang tidak terlalu bergantung pada hutang
3. ROE tinggi - perusahaan yang efisien menggunakan modal
4. Profit margin tinggi - pricing power
5. Dividen konsisten - shareholder friendly
6. Trend harga naik - market mengakui nilai perusahaan
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from config import SCORING_WEIGHTS, MIN_CRITERIA


class BuffettScorer:
    """
    Sistem scoring saham berdasarkan prinsip investasi Warren Buffett
    """

    def __init__(self, weights: Dict = None):
        self.weights = weights or SCORING_WEIGHTS

    def normalize_score(self, value: float, min_val: float, max_val: float,
                       inverse: bool = False) -> float:
        """
        Normalisasi nilai ke skala 0-100

        Args:
            value: Nilai yang akan dinormalisasi
            min_val: Nilai minimum dalam dataset
            max_val: Nilai maksimum dalam dataset
            inverse: True jika nilai rendah lebih baik (seperti D/E ratio)

        Returns:
            Skor dalam skala 0-100
        """
        if pd.isna(value) or value is None:
            return 0

        if max_val == min_val:
            return 50

        # Normalisasi ke 0-100
        normalized = (value - min_val) / (max_val - min_val) * 100

        # Jika inverse (rendah lebih baik), balik skornya
        if inverse:
            normalized = 100 - normalized

        # Batasi antara 0-100
        return max(0, min(100, normalized))

    def calculate_individual_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Hitung skor individual untuk setiap metrik

        Returns:
            DataFrame dengan kolom skor tambahan
        """
        result = df.copy()

        # 1. Skor Trend Harga 1 Tahun (tinggi lebih baik)
        if 'price_change_1y' in df.columns:
            min_val = df['price_change_1y'].min()
            max_val = df['price_change_1y'].max()
            result['score_price_trend'] = df['price_change_1y'].apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 2. Skor Debt to Equity (rendah lebih baik)
        if 'debt_to_equity' in df.columns:
            # Untuk D/E, kita batasi maksimal di 3 untuk normalisasi yang lebih baik
            de_capped = df['debt_to_equity'].clip(upper=3)
            min_val = de_capped.min()
            max_val = de_capped.max()
            result['score_debt'] = de_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=True)
            )

        # 3. Skor ROE (tinggi lebih baik)
        if 'roe' in df.columns:
            # ROE yang terlalu tinggi (>50%) bisa jadi anomali
            roe_capped = df['roe'].clip(lower=-20, upper=50)
            min_val = roe_capped.min()
            max_val = roe_capped.max()
            result['score_roe'] = roe_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 4. Skor Profit Margin (tinggi lebih baik)
        if 'profit_margin' in df.columns:
            margin_capped = df['profit_margin'].clip(lower=-20, upper=50)
            min_val = margin_capped.min()
            max_val = margin_capped.max()
            result['score_margin'] = margin_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 5. Skor Dividend Yield (tinggi lebih baik, tapi tidak terlalu tinggi)
        if 'dividend_yield' in df.columns:
            # Dividend yield > 10% bisa jadi warning
            div_capped = df['dividend_yield'].clip(upper=10)
            min_val = 0
            max_val = div_capped.max()
            result['score_dividend'] = div_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 6. Skor Current Ratio (tinggi lebih baik, tapi tidak terlalu tinggi)
        if 'current_ratio' in df.columns:
            # Current ratio > 3 tidak memberikan nilai tambah
            cr_capped = df['current_ratio'].clip(upper=3)
            min_val = 0
            max_val = cr_capped.max()
            result['score_liquidity'] = cr_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 7. Skor Earnings Growth (tinggi lebih baik)
        if 'earnings_growth' in df.columns:
            eg_capped = df['earnings_growth'].clip(lower=-50, upper=100)
            min_val = eg_capped.min()
            max_val = eg_capped.max()
            result['score_growth'] = eg_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        return result

    def calculate_buffett_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Hitung skor total Buffett berdasarkan bobot yang ditentukan

        Formula:
        Buffett Score = (w1 × Price Trend Score) +
                       (w2 × Debt Score) +
                       (w3 × ROE Score) +
                       (w4 × Margin Score) +
                       (w5 × Dividend Score) +
                       (w6 × Liquidity Score) +
                       (w7 × Growth Score)

        Returns:
            DataFrame dengan kolom buffett_score
        """
        # Hitung skor individual dulu
        result = self.calculate_individual_scores(df)

        # Mapping kolom skor ke bobot
        score_mapping = {
            'score_price_trend': 'price_trend_1y',
            'score_debt': 'debt_to_equity',
            'score_roe': 'roe',
            'score_margin': 'profit_margin',
            'score_dividend': 'dividend_yield',
            'score_liquidity': 'current_ratio',
            'score_growth': 'earnings_growth'
        }

        # Hitung skor total
        total_weight = 0
        result['buffett_score'] = 0

        for score_col, weight_key in score_mapping.items():
            if score_col in result.columns and weight_key in self.weights:
                weight = self.weights[weight_key]
                result['buffett_score'] += result[score_col].fillna(0) * weight
                total_weight += weight

        # Normalisasi jika total bobot tidak sama dengan 1
        if total_weight > 0:
            result['buffett_score'] = result['buffett_score'] / total_weight

        return result

    def apply_buffett_filter(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Filter saham berdasarkan kriteria minimum Warren Buffett

        Returns:
            Tuple (saham yang lolos filter, saham yang tidak lolos)
        """
        filtered = df.copy()
        reasons = []

        # 1. Filter berdasarkan trend harga (harus naik)
        mask_trend = filtered['price_change_1y'] > 0
        filtered.loc[~mask_trend, 'filter_reason'] = 'Trend harga turun'

        # 2. Filter ROE minimum
        if 'roe' in filtered.columns:
            mask_roe = (filtered['roe'] >= MIN_CRITERIA['min_roe']) | filtered['roe'].isna()
            filtered.loc[~mask_roe & mask_trend, 'filter_reason'] = 'ROE terlalu rendah'

        # 3. Filter D/E ratio maksimum
        if 'debt_to_equity' in filtered.columns:
            mask_de = (filtered['debt_to_equity'] <= MIN_CRITERIA['max_debt_to_equity']) | filtered['debt_to_equity'].isna()
            filtered.loc[~mask_de & mask_trend & mask_roe, 'filter_reason'] = 'Hutang terlalu tinggi'

        # 4. Filter profit margin minimum
        if 'profit_margin' in filtered.columns:
            mask_margin = (filtered['profit_margin'] >= MIN_CRITERIA['min_profit_margin']) | filtered['profit_margin'].isna()

        # 5. Filter dividend yield minimum
        if 'dividend_yield' in filtered.columns:
            mask_div = (filtered['dividend_yield'] >= MIN_CRITERIA['min_dividend_yield']) | filtered['dividend_yield'].isna()

        # Saham yang lolos semua kriteria
        passed = filtered[
            (filtered['price_change_1y'] > 0)  # Trend naik
        ].copy()

        failed = filtered[~filtered.index.isin(passed.index)].copy()

        return passed, failed

    def get_ranking(self, df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Dapatkan ranking top N saham berdasarkan Buffett Score

        Args:
            df: DataFrame hasil scoring
            top_n: Jumlah saham teratas yang ingin ditampilkan

        Returns:
            DataFrame dengan ranking
        """
        # Filter dan hitung skor
        passed, _ = self.apply_buffett_filter(df)
        scored = self.calculate_buffett_score(passed)

        # Sort berdasarkan skor dan ambil top N
        ranked = scored.sort_values('buffett_score', ascending=False).head(top_n)
        ranked['rank'] = range(1, len(ranked) + 1)

        return ranked


def explain_buffett_formula():
    """
    Menjelaskan formula scoring Warren Buffett
    """
    explanation = """
╔══════════════════════════════════════════════════════════════════════════════╗
║              FORMULA SCORING SAHAM ALA WARREN BUFFETT                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  BUFFETT SCORE = Σ (Wi × Si)                                                 ║
║                                                                              ║
║  Dimana:                                                                     ║
║  Wi = Bobot untuk metrik i                                                   ║
║  Si = Skor ternormalisasi (0-100) untuk metrik i                            ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  KOMPONEN SCORING:                                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. TREND HARGA 1 TAHUN (15%)                                               ║
║     - Mengukur momentum harga dalam 1 tahun terakhir                        ║
║     - Rumus: ((Harga Akhir - Harga Awal) / Harga Awal) × 100                ║
║     - Semakin tinggi return, semakin tinggi skor                            ║
║                                                                              ║
║  2. DEBT TO EQUITY RATIO (20%)                                              ║
║     - Mengukur tingkat hutang perusahaan                                    ║
║     - D/E = Total Hutang / Total Ekuitas                                    ║
║     - Semakin RENDAH, semakin BAIK (inverse scoring)                        ║
║     - Warren Buffett suka perusahaan dengan hutang minimal                  ║
║                                                                              ║
║  3. RETURN ON EQUITY - ROE (20%)                                            ║
║     - Mengukur efisiensi penggunaan modal                                   ║
║     - ROE = Laba Bersih / Ekuitas × 100%                                    ║
║     - Target Buffett: ROE > 15%                                             ║
║     - Menunjukkan kemampuan perusahaan menghasilkan profit dari modal       ║
║                                                                              ║
║  4. PROFIT MARGIN (15%)                                                      ║
║     - Mengukur profitabilitas per rupiah penjualan                          ║
║     - Net Profit Margin = Laba Bersih / Pendapatan × 100%                   ║
║     - Menunjukkan pricing power dan efisiensi operasional                   ║
║                                                                              ║
║  5. DIVIDEND YIELD (15%)                                                     ║
║     - Mengukur return dari dividen                                          ║
║     - Dividend Yield = Dividen per Saham / Harga Saham × 100%               ║
║     - Menunjukkan komitmen perusahaan membagi keuntungan ke pemegang saham  ║
║                                                                              ║
║  6. CURRENT RATIO (10%)                                                      ║
║     - Mengukur kemampuan membayar kewajiban jangka pendek                   ║
║     - Current Ratio = Aset Lancar / Kewajiban Lancar                        ║
║     - Idealnya > 1.5                                                         ║
║                                                                              ║
║  7. EARNINGS GROWTH (5%)                                                     ║
║     - Mengukur pertumbuhan laba                                             ║
║     - Semakin tinggi pertumbuhan, semakin baik                              ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  KRITERIA FILTER (Syarat Minimum):                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ✓ Trend harga 1 tahun: HARUS POSITIF (naik)                                ║
║  ✓ D/E Ratio: Maksimal 1.0 (hutang tidak melebihi modal)                    ║
║  ✓ ROE: Minimal 15%                                                          ║
║  ✓ Profit Margin: Minimal 10%                                                ║
║  ✓ Dividend Yield: Minimal 1%                                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PRINSIP WARREN BUFFETT YANG DIGUNAKAN:                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  "Rule No. 1: Never lose money. Rule No. 2: Never forget Rule No. 1"        ║
║  → Fokus pada perusahaan dengan fundamental kuat dan hutang rendah          ║
║                                                                              ║
║  "It's far better to buy a wonderful company at a fair price than a fair    ║
║   company at a wonderful price"                                              ║
║  → Prioritaskan kualitas perusahaan (ROE, profit margin) di atas valuasi    ║
║                                                                              ║
║  "Our favorite holding period is forever"                                    ║
║  → Cari perusahaan yang bisa memberi dividen konsisten                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    return explanation
