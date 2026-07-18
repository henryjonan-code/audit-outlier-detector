"""
Sistem Scoring Saham ala Warren Buffett V5.1 - REVISED

============================================================================
UPDATE V5.1 - REVISED CRITERIA (Juni 2026):
============================================================================
Revisi dari V5.0 berdasarkan feedback:
- D/E < 0.5 terlalu ketat → dinaikkan ke < 1.0
- FCF dijadikan soft filter untuk capex-heavy industries
- Ditambah weighted soft scoring system

7 HARD FILTER:
1. Profitabilitas: ROE >= 10%
2. Utang sehat: D/E < 100% (non-bank) atau CAR/NPL sehat (bank)
3. Arus kas: Operating Cash Flow positif
4. Dividen: Yield > 0%, Payout Ratio < 80%
5. Likuiditas: Volume cukup, Market Cap > 5T
6. Free Float: >= 15%
7. Governance: Tidak ada red flag

SOFT FILTER (weighted scoring, bukan eliminasi):
- FCF > 0: +15 pts
- Revenue growth 3Y > 0: +10 pts
- Dividend streak 3Y: +15 pts
- Price trend 1Y > 0: +10 pts

============================================================================
HISTORY:
- V4.0: 5 Hard Filter (trend, D/E, dividend, ROE>0, profit)
- V3.0: Bank metrics (CAR, NPL, NIM)
- V2.0: Valuation Score + Liquidity Filter
- V1.0: Basic Buffett criteria
============================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from config import SCORING_WEIGHTS, MIN_CRITERIA, LIQUIDITY_CRITERIA, VALUATION_BENCHMARKS


class BuffettScorer:
    """
    Sistem scoring saham berdasarkan prinsip investasi Warren Buffett V2.0
    Dengan Valuation Score dan Liquidity Filter
    """

    def __init__(self, weights: Dict = None):
        self.weights = weights or SCORING_WEIGHTS

    def normalize_score(self, value: float, min_val: float, max_val: float,
                       inverse: bool = False) -> float:
        """
        Normalisasi nilai ke skala 0-100
        """
        if pd.isna(value) or value is None:
            return 0

        if max_val == min_val:
            return 50

        normalized = (value - min_val) / (max_val - min_val) * 100

        if inverse:
            normalized = 100 - normalized

        return max(0, min(100, normalized))

    def is_bank(self, row: pd.Series) -> bool:
        """
        Cek apakah saham adalah bank
        """
        is_bank_field = row.get('is_bank')
        # Handle nan/None values properly
        if pd.notna(is_bank_field) and is_bank_field == True:
            return True
        industry = row.get('industry', '')
        return 'Bank' in str(industry)

    def calculate_bank_health_score(self, row: pd.Series) -> float:
        """
        Hitung skor kesehatan bank berdasarkan metrik khusus bank

        Metrik Bank (BUKAN D/E ratio!):
        - CAR (Capital Adequacy Ratio): min 8%, ideal >20% (bobot 30%)
        - NPL (Non Performing Loan): max 5%, ideal <2% (bobot 30%)
        - NIM (Net Interest Margin): ideal >4% (bobot 20%)
        - Cost to Income Ratio: ideal <50% (bobot 20%)

        Returns:
            Skor kesehatan bank 0-100
        """
        scores = []
        weights = []

        # 1. CAR Score (30%) - Capital Adequacy Ratio
        car = row.get('car')
        if pd.notna(car) and car is not None:
            if car >= 25:
                car_score = 100
            elif car >= 20:
                car_score = 80
            elif car >= 15:
                car_score = 60
            elif car >= 8:  # Minimum requirement
                car_score = 40
            else:
                car_score = 0  # Di bawah minimum!
            scores.append(car_score)
            weights.append(0.3)

        # 2. NPL Score (30%) - Non Performing Loan (INVERSE - rendah lebih baik)
        npl = row.get('npl')
        if pd.notna(npl) and npl is not None:
            if npl <= 1:
                npl_score = 100
            elif npl <= 2:
                npl_score = 80
            elif npl <= 3:
                npl_score = 60
            elif npl <= 5:  # Maximum allowed
                npl_score = 40
            else:
                npl_score = 0  # Di atas maximum!
            scores.append(npl_score)
            weights.append(0.3)

        # 3. NIM Score (20%) - Net Interest Margin
        nim = row.get('nim')
        if pd.notna(nim) and nim is not None:
            if nim >= 6:
                nim_score = 100
            elif nim >= 5:
                nim_score = 80
            elif nim >= 4:
                nim_score = 60
            elif nim >= 3:
                nim_score = 40
            else:
                nim_score = 20
            scores.append(nim_score)
            weights.append(0.2)

        # 4. Cost to Income Score (20%) - INVERSE - rendah lebih baik
        cti = row.get('cost_to_income')
        if pd.notna(cti) and cti is not None:
            if cti <= 30:
                cti_score = 100
            elif cti <= 40:
                cti_score = 80
            elif cti <= 50:
                cti_score = 60
            elif cti <= 60:
                cti_score = 40
            else:
                cti_score = 20
            scores.append(cti_score)
            weights.append(0.2)

        if not scores:
            return 50  # Default jika tidak ada data

        total_weight = sum(weights)
        return sum(s * w for s, w in zip(scores, weights)) / total_weight

    def calculate_valuation_score(self, row: pd.Series) -> float:
        """
        Hitung Valuation Score berdasarkan PEG, P/E, dan P/B ratio

        Komponen:
        - PEG Ratio (40%): < 1 = undervalued, > 2 = overvalued
        - P/E Ratio (30%): Dibandingkan dengan benchmark sektor
        - P/B Ratio (30%): < 2 ideal untuk value investing

        Returns:
            Skor valuasi 0-100
        """
        scores = []
        weights = []

        # 1. PEG Ratio Score (40% dari valuation)
        peg = row.get('peg_ratio')
        if pd.notna(peg) and peg is not None and peg > 0:
            # PEG < 0.5 = 100, PEG = 1 = 50, PEG > 2 = 0
            if peg <= 0.5:
                peg_score = 100
            elif peg <= 1:
                peg_score = 100 - (peg - 0.5) * 100  # Linear dari 100 ke 50
            elif peg <= 2:
                peg_score = 50 - (peg - 1) * 50  # Linear dari 50 ke 0
            else:
                peg_score = 0
            scores.append(peg_score)
            weights.append(0.4)

        # 2. P/E Ratio Score (30% dari valuation)
        pe = row.get('pe_ratio')
        sector = row.get('sector', '')
        sector_pe = VALUATION_BENCHMARKS['sector_pe'].get(sector, 15)

        if pd.notna(pe) and pe is not None and pe > 0:
            # P/E di bawah sektor = bagus, di atas = kurang bagus
            pe_ratio_vs_sector = pe / sector_pe
            if pe_ratio_vs_sector <= 0.5:
                pe_score = 100
            elif pe_ratio_vs_sector <= 1:
                pe_score = 100 - (pe_ratio_vs_sector - 0.5) * 60
            elif pe_ratio_vs_sector <= 1.5:
                pe_score = 70 - (pe_ratio_vs_sector - 1) * 80
            else:
                pe_score = max(0, 30 - (pe_ratio_vs_sector - 1.5) * 30)
            scores.append(pe_score)
            weights.append(0.3)

        # 3. P/B Ratio Score (30% dari valuation)
        pb = row.get('pb_ratio')
        if pd.notna(pb) and pb is not None and pb > 0:
            # P/B < 1 = 100, P/B = 2 = 50, P/B > 4 = 0
            if pb <= 1:
                pb_score = 100
            elif pb <= 2:
                pb_score = 100 - (pb - 1) * 50
            elif pb <= 4:
                pb_score = 50 - (pb - 2) * 25
            else:
                pb_score = 0
            scores.append(pb_score)
            weights.append(0.3)

        if not scores:
            return 50  # Default jika tidak ada data

        # Weighted average
        total_weight = sum(weights)
        return sum(s * w for s, w in zip(scores, weights)) / total_weight

    def calculate_liquidity_score(self, row: pd.Series) -> float:
        """
        Hitung Liquidity Score untuk menilai seberapa liquid saham

        Komponen:
        - Average Daily Volume (50%)
        - Market Cap (30%)
        - Free Float (20%)

        Returns:
            Skor likuiditas 0-100
        """
        scores = []
        weights = []

        # 1. Volume Score (50%)
        avg_vol = row.get('avg_volume')
        min_vol = LIQUIDITY_CRITERIA['min_avg_volume']

        if pd.notna(avg_vol) and avg_vol is not None:
            if avg_vol >= min_vol * 10:  # > 10 juta
                vol_score = 100
            elif avg_vol >= min_vol * 5:  # > 5 juta
                vol_score = 80
            elif avg_vol >= min_vol:  # > 1 juta
                vol_score = 60
            elif avg_vol >= min_vol * 0.5:  # > 500k
                vol_score = 40
            else:
                vol_score = 20
            scores.append(vol_score)
            weights.append(0.5)

        # 2. Market Cap Score (30%)
        mcap = row.get('market_cap')
        min_mcap = LIQUIDITY_CRITERIA['min_market_cap']

        if pd.notna(mcap) and mcap is not None:
            if mcap >= min_mcap * 20:  # > 100T
                mcap_score = 100
            elif mcap >= min_mcap * 10:  # > 50T
                mcap_score = 80
            elif mcap >= min_mcap * 2:  # > 10T
                mcap_score = 60
            elif mcap >= min_mcap:  # > 5T
                mcap_score = 40
            else:
                mcap_score = 20
            scores.append(mcap_score)
            weights.append(0.3)

        # 3. Free Float Score (20%)
        ff = row.get('free_float_pct')
        min_ff = LIQUIDITY_CRITERIA['min_free_float_pct']

        if pd.notna(ff) and ff is not None:
            if ff >= 40:
                ff_score = 100
            elif ff >= 30:
                ff_score = 80
            elif ff >= min_ff:
                ff_score = 60
            else:
                ff_score = 30
            scores.append(ff_score)
            weights.append(0.2)

        if not scores:
            return 50

        total_weight = sum(weights)
        return sum(s * w for s, w in zip(scores, weights)) / total_weight

    def calculate_individual_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Hitung skor individual untuk setiap metrik
        """
        result = df.copy()

        # 1. Skor Trend Harga 3 TAHUN (lebih reliable untuk menilai performa jangka panjang)
        if 'price_change_3y' in df.columns:
            min_val = df['price_change_3y'].min()
            max_val = df['price_change_3y'].max()
            result['score_price_trend'] = df['price_change_3y'].apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 2. Skor Debt/Health (berbeda untuk bank vs non-bank!)
        # Bank: gunakan bank_health_score (CAR, NPL, NIM)
        # Non-Bank: gunakan debt_to_equity
        result['score_debt'] = df.apply(
            lambda row: self.calculate_bank_health_score(row) if self.is_bank(row)
            else self.normalize_score(
                row.get('debt_to_equity', 1),
                0, 3, inverse=True
            ) if pd.notna(row.get('debt_to_equity')) else 50,
            axis=1
        )

        # 3. Skor ROE
        if 'roe' in df.columns:
            roe_capped = df['roe'].clip(lower=-20, upper=50)
            min_val = roe_capped.min()
            max_val = roe_capped.max()
            result['score_roe'] = roe_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 4. Skor Profit Margin
        if 'profit_margin' in df.columns:
            margin_capped = df['profit_margin'].clip(lower=-20, upper=50)
            min_val = margin_capped.min()
            max_val = margin_capped.max()
            result['score_margin'] = margin_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 5. Skor Dividend Yield
        if 'dividend_yield' in df.columns:
            div_capped = df['dividend_yield'].clip(upper=15)
            min_val = 0
            max_val = div_capped.max()
            result['score_dividend'] = div_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 6. Skor Current Ratio (Liquidity Ratio)
        if 'current_ratio' in df.columns:
            cr_capped = df['current_ratio'].clip(upper=3)
            min_val = 0
            max_val = cr_capped.max()
            result['score_current_ratio'] = cr_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 7. Skor Earnings Growth
        if 'earnings_growth' in df.columns:
            eg_capped = df['earnings_growth'].clip(lower=-50, upper=100)
            min_val = eg_capped.min()
            max_val = eg_capped.max()
            result['score_growth'] = eg_capped.apply(
                lambda x: self.normalize_score(x, min_val, max_val, inverse=False)
            )

        # 8. NEW: Skor Valuation
        result['score_valuation'] = df.apply(self.calculate_valuation_score, axis=1)

        # 9. NEW: Skor Trading Liquidity
        result['score_trading_liq'] = df.apply(self.calculate_liquidity_score, axis=1)

        return result

    def calculate_buffett_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Hitung skor total Buffett V2.0 dengan Valuation dan Liquidity

        Formula V2.0:
        BUFFETT SCORE = (0.15 × Debt) + (0.15 × ROE) + (0.10 × Trend) +
                        (0.10 × Margin) + (0.10 × Dividend) + (0.05 × Current Ratio) +
                        (0.05 × Growth) + (0.25 × Valuation) + (0.05 × Trading Liq)
        """
        result = self.calculate_individual_scores(df)

        # Mapping skor ke bobot
        score_mapping = {
            'score_price_trend': 'price_trend_3y',  # Changed to 3 years
            'score_debt': 'debt_to_equity',
            'score_roe': 'roe',
            'score_margin': 'profit_margin',
            'score_dividend': 'dividend_yield',
            'score_current_ratio': 'current_ratio',
            'score_growth': 'earnings_growth',
            'score_valuation': 'valuation',
            'score_trading_liq': 'liquidity',
        }

        total_weight = 0
        result['buffett_score'] = 0

        for score_col, weight_key in score_mapping.items():
            if score_col in result.columns and weight_key in self.weights:
                weight = self.weights[weight_key]
                result['buffett_score'] += result[score_col].fillna(0) * weight
                total_weight += weight

        if total_weight > 0:
            result['buffett_score'] = result['buffett_score'] / total_weight

        return result

    def apply_liquidity_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter saham dengan likuiditas rendah (mudah digoreng)
        """
        filtered = df.copy()

        # Filter Market Cap
        if 'market_cap' in filtered.columns:
            min_mcap = LIQUIDITY_CRITERIA['min_market_cap']
            filtered = filtered[
                (filtered['market_cap'] >= min_mcap) |
                (filtered['market_cap'].isna())
            ]

        # Filter Volume
        if 'avg_volume' in filtered.columns:
            min_vol = LIQUIDITY_CRITERIA['min_avg_volume']
            filtered = filtered[
                (filtered['avg_volume'] >= min_vol) |
                (filtered['avg_volume'].isna())
            ]

        return filtered

    def apply_buffett_filter(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Filter saham berdasarkan kriteria KETAT V5.0 - POST MSCI:

        7 HARD FILTER:
        1. Profitabilitas: ROE >= 10% (bukan cuma > 0%)
        2. Utang sehat: D/E < 50% untuk non-bank, atau metrik bank sehat
        3. Arus kas: Operating Cash Flow positif (jika data ada)
        4. Dividen: Yield > 0%, Payout Ratio < 80%
        5. Likuiditas: Volume cukup, Market Cap > 5T
        6. Free Float: >= 15%
        7. Governance: Tidak ada red flag (governance_flag != True)

        SOFT FILTER (untuk scoring, bukan eliminasi):
        - Trend 1Y/3Y positif (momentum)
        - Valuasi wajar (PER < 20, PBV < 3)

        Tidak ada toleransi - semua HARD FILTER HARUS terpenuhi!
        """
        # Apply liquidity filter first
        filtered = self.apply_liquidity_filter(df)

        # =====================================================================
        # HARD FILTER 1: ROE >= 10% (Profitabilitas berkualitas)
        # =====================================================================
        has_roe = 'roe' in filtered.columns
        if has_roe:
            mask_roe = filtered['roe'] >= 10
        else:
            mask_roe = pd.Series([True] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 2: D/E < 100% untuk NON-BANK (revised dari 50%)
        # Bank punya struktur modal berbeda, gunakan CAR/NPL
        # Catatan V5.1: 50% terlalu ketat, banyak perusahaan sehat punya leverage
        # =====================================================================
        if 'debt_to_equity' in filtered.columns:
            is_bank = filtered.apply(lambda row: self.is_bank(row), axis=1)
            de_ok = (filtered['debt_to_equity'] < 1.0) | filtered['debt_to_equity'].isna()
            mask_de = is_bank | de_ok
        else:
            mask_de = pd.Series([True] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 3: Operating Cash Flow positif
        # STRICT: None/missing = FAIL (bukan skip)
        # =====================================================================
        if 'operating_cash_flow' in filtered.columns:
            mask_ocf = filtered['operating_cash_flow'] > 0
        else:
            mask_ocf = pd.Series([False] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 4: Bagi dividen + Payout ratio sustainable
        # STRICT: None payout = FAIL
        # =====================================================================
        if 'dividend_yield' in filtered.columns:
            mask_div = filtered['dividend_yield'] > 0
        else:
            mask_div = pd.Series([True] * len(filtered), index=filtered.index)

        if 'payout_ratio' in filtered.columns:
            mask_payout = filtered['payout_ratio'] < 80
        else:
            mask_payout = pd.Series([False] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 5: Free Float >= 15% (MSCI requirement)
        # =====================================================================
        if 'free_float_pct' in filtered.columns:
            mask_float = (filtered['free_float_pct'] >= 15) | filtered['free_float_pct'].isna()
        else:
            mask_float = pd.Series([True] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 6: Governance - tidak ada red flag
        # =====================================================================
        if 'governance_flag' in filtered.columns:
            # governance_flag = True berarti ada masalah, harus skip
            mask_gov = (filtered['governance_flag'] != True) | filtered['governance_flag'].isna()
        else:
            mask_gov = pd.Series([True] * len(filtered), index=filtered.index)

        # =====================================================================
        # HARD FILTER 7: Valuasi wajar (PER < 20 atau PBV < 3)
        # =====================================================================
        has_per = 'pe_ratio' in filtered.columns
        has_pbv = 'pb_ratio' in filtered.columns
        if has_per and has_pbv:
            mask_val = (filtered['pe_ratio'] < 20) | (filtered['pb_ratio'] < 3) | \
                       filtered['pe_ratio'].isna() | filtered['pb_ratio'].isna()
        elif has_per:
            mask_val = (filtered['pe_ratio'] < 20) | filtered['pe_ratio'].isna()
        elif has_pbv:
            mask_val = (filtered['pb_ratio'] < 3) | filtered['pb_ratio'].isna()
        else:
            mask_val = pd.Series([True] * len(filtered), index=filtered.index)

        # =====================================================================
        # SOFT FILTER: Trend positif (untuk ranking, bukan eliminasi)
        # Catatan: Dihapus dari hard filter agar tidak miss opportunity
        # pada saham quality yang sedang turun
        # =====================================================================

        # GABUNGKAN SEMUA HARD FILTER
        mask_all = mask_roe & mask_de & mask_ocf & mask_div & mask_payout & \
                   mask_float & mask_gov & mask_val

        passed = filtered[mask_all].copy()
        failed = filtered[~mask_all].copy()

        return passed, failed

    def get_ranking(self, df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Dapatkan ranking top N saham berdasarkan Buffett Score V2.0
        """
        passed, _ = self.apply_buffett_filter(df)
        scored = self.calculate_buffett_score(passed)

        ranked = scored.sort_values('buffett_score', ascending=False).head(top_n)
        ranked['rank'] = range(1, len(ranked) + 1)

        return ranked

    def get_valuation_status(self, row: pd.Series) -> str:
        """
        Tentukan status valuasi saham
        """
        peg = row.get('peg_ratio')
        pe = row.get('pe_ratio')
        pb = row.get('pb_ratio')

        if pd.notna(peg) and peg < 1:
            return "UNDERVALUED"
        elif pd.notna(peg) and peg < 1.5:
            return "FAIR VALUE"
        elif pd.notna(pe) and pe < 10:
            return "CHEAP P/E"
        elif pd.notna(pb) and pb < 1:
            return "BELOW BOOK"
        elif pd.notna(peg) and peg > 2:
            return "OVERVALUED"
        else:
            return "FAIR"

    def get_liquidity_status(self, row: pd.Series) -> str:
        """
        Tentukan status likuiditas saham
        """
        mcap = row.get('market_cap', 0) or 0
        vol = row.get('avg_volume', 0) or 0

        if mcap >= 100e12 and vol >= 20_000_000:
            return "SANGAT LIQUID"
        elif mcap >= 20e12 and vol >= 5_000_000:
            return "LIQUID"
        elif mcap >= 5e12 and vol >= 1_000_000:
            return "CUKUP LIQUID"
        else:
            return "KURANG LIQUID"


def explain_buffett_formula():
    """
    Menjelaskan formula scoring Warren Buffett V2.0
    """
    explanation = """
╔══════════════════════════════════════════════════════════════════════════════╗
║          FORMULA SCORING SAHAM ALA WARREN BUFFETT V2.0                       ║
║          (Dengan Valuation Score & Liquidity Filter)                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  BUFFETT SCORE = Σ (Wi × Si)                                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  KOMPONEN SCORING V2.0:                                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. VALUATION SCORE (25%) ← NEW! BOBOT BESAR                                ║
║     Komponen:                                                                ║
║     • PEG Ratio (40%): P/E dibagi Growth Rate                               ║
║       - PEG < 0.5 = SUPER MURAH (Score 100)                                 ║
║       - PEG < 1.0 = UNDERVALUED (Score 50-100)                              ║
║       - PEG 1-2   = FAIR VALUE (Score 0-50)                                 ║
║       - PEG > 2   = OVERVALUED (Score 0)                                    ║
║     • P/E Ratio (30%): Dibandingkan dengan P/E sektor                       ║
║     • P/B Ratio (30%): Price to Book Value                                  ║
║       - P/B < 1 = BELOW BOOK VALUE (Score 100)                              ║
║       - P/B < 2 = FAIR (Score 50-100)                                       ║
║                                                                              ║
║  2. DEBT TO EQUITY (15%)                                                     ║
║     - D/E < 0.5 = Sangat Baik                                               ║
║     - D/E < 1.0 = Baik                                                      ║
║     - D/E > 1.0 = Perlu perhatian                                           ║
║                                                                              ║
║  3. RETURN ON EQUITY - ROE (15%)                                            ║
║     - ROE > 20% = Excellent                                                  ║
║     - ROE > 15% = Good                                                       ║
║     - ROE < 10% = Poor                                                       ║
║                                                                              ║
║  4. TREND HARGA 3 TAHUN (10%)                                               ║
║  5. PROFIT MARGIN (10%)                                                      ║
║  6. DIVIDEND YIELD (10%)                                                     ║
║  7. CURRENT RATIO (5%)                                                       ║
║  8. EARNINGS GROWTH (5%)                                                     ║
║  9. TRADING LIQUIDITY (5%) ← NEW! ANTI-GORENG                               ║
║     • Average Daily Volume                                                   ║
║     • Market Cap                                                             ║
║     • Free Float Percentage                                                  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  LIQUIDITY FILTER (Anti-Goreng):                                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ✓ Market Cap minimal: Rp 5 Triliun                                         ║
║  ✓ Avg Daily Volume minimal: 1 Juta lembar/hari                             ║
║  ✓ Free Float minimal: 15%                                                   ║
║                                                                              ║
║  Saham dengan likuiditas rendah mudah DIGORENG (dimanipulasi harga)         ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  PRINSIP WARREN BUFFETT:                                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  "Price is what you pay. Value is what you get."                            ║
║  → Gunakan PEG < 1 untuk cari saham undervalued                             ║
║                                                                              ║
║  "Be fearful when others are greedy, greedy when others are fearful."       ║
║  → Beli saham bagus saat harga turun (PEG rendah)                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    return explanation
