"""
Modul untuk mengambil data saham dari Yahoo Finance API
(Tanpa ketergantungan pada yfinance library)
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import time


class StockDataFetcher:
    """Kelas untuk mengambil data fundamental dan harga saham"""

    def __init__(self):
        self.cache = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_quote_summary(self, ticker: str) -> Optional[Dict]:
        """
        Mengambil data quote summary dari Yahoo Finance

        Args:
            ticker: Kode saham (contoh: BBCA.JK)

        Returns:
            Dictionary berisi data fundamental
        """
        try:
            # Yahoo Finance API endpoint untuk quote summary
            modules = [
                'price', 'summaryDetail', 'defaultKeyStatistics',
                'financialData', 'calendarEvents', 'assetProfile'
            ]
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
            params = {
                'modules': ','.join(modules)
            }

            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None

            data = response.json()
            if 'quoteSummary' not in data or not data['quoteSummary'].get('result'):
                return None

            return data['quoteSummary']['result'][0]

        except Exception as e:
            print(f"    Error fetching quote summary: {str(e)[:50]}")
            return None

    def get_historical_prices(self, ticker: str, days: int = 365) -> Optional[pd.DataFrame]:
        """
        Mengambil data harga historis dari Yahoo Finance

        Args:
            ticker: Kode saham (contoh: BBCA.JK)
            days: Jumlah hari ke belakang

        Returns:
            DataFrame dengan data harga
        """
        try:
            end_date = int(datetime.now().timestamp())
            start_date = int((datetime.now() - timedelta(days=days)).timestamp())

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                'period1': start_date,
                'period2': end_date,
                'interval': '1d',
                'events': 'history'
            }

            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None

            data = response.json()
            if 'chart' not in data or not data['chart'].get('result'):
                return None

            result = data['chart']['result'][0]
            timestamps = result.get('timestamp', [])
            quotes = result.get('indicators', {}).get('quote', [{}])[0]

            if not timestamps or not quotes:
                return None

            df = pd.DataFrame({
                'timestamp': timestamps,
                'open': quotes.get('open', []),
                'high': quotes.get('high', []),
                'low': quotes.get('low', []),
                'close': quotes.get('close', []),
                'volume': quotes.get('volume', [])
            })

            df['date'] = pd.to_datetime(df['timestamp'], unit='s')
            return df

        except Exception as e:
            print(f"    Error fetching history: {str(e)[:50]}")
            return None

    def extract_value(self, data: Dict, key: str, subkey: str = 'raw') -> Optional[float]:
        """
        Extract value from nested Yahoo Finance data structure

        Args:
            data: Dictionary containing the data
            key: Key to look for
            subkey: Usually 'raw' for numeric values

        Returns:
            The extracted value or None
        """
        try:
            if data is None:
                return None
            value = data.get(key, {})
            if isinstance(value, dict):
                return value.get(subkey)
            return value
        except:
            return None

    def get_stock_data(self, ticker: str) -> Optional[Dict]:
        """
        Mengambil semua data yang diperlukan untuk satu saham

        Args:
            ticker: Kode saham (contoh: BBCA.JK)

        Returns:
            Dictionary berisi data fundamental dan harga
        """
        try:
            # Ambil quote summary
            summary = self.get_quote_summary(ticker)
            if not summary:
                return None

            # Ambil data harga historis
            hist = self.get_historical_prices(ticker)
            if hist is None or len(hist) < 50:
                return None

            # Extract data dari summary
            price_data = summary.get('price', {})
            summary_detail = summary.get('summaryDetail', {})
            key_stats = summary.get('defaultKeyStatistics', {})
            financial_data = summary.get('financialData', {})
            asset_profile = summary.get('assetProfile', {})

            # Hitung price trend 1 tahun
            valid_closes = hist['close'].dropna()
            if len(valid_closes) < 50:
                return None

            price_start = valid_closes.iloc[0]
            price_end = valid_closes.iloc[-1]

            if price_start == 0 or pd.isna(price_start):
                return None

            price_change_1y = ((price_end - price_start) / price_start) * 100

            # Extract fundamental data
            data = {
                'ticker': ticker,
                'name': price_data.get('shortName') or price_data.get('longName', ticker),
                'sector': asset_profile.get('sector', 'N/A'),
                'industry': asset_profile.get('industry', 'N/A'),

                # Harga
                'current_price': self.extract_value(price_data, 'regularMarketPrice') or price_end,
                'price_change_1y': price_change_1y,
                'price_start_1y': price_start,
                'price_end_1y': price_end,

                # Rasio Hutang
                'debt_to_equity': self.extract_value(financial_data, 'debtToEquity'),
                'total_debt': self.extract_value(financial_data, 'totalDebt'),
                'total_cash': self.extract_value(financial_data, 'totalCash'),

                # Profitabilitas
                'roe': self.extract_value(financial_data, 'returnOnEquity'),
                'roa': self.extract_value(financial_data, 'returnOnAssets'),
                'profit_margin': self.extract_value(financial_data, 'profitMargins'),
                'operating_margin': self.extract_value(financial_data, 'operatingMargins'),
                'gross_margin': self.extract_value(financial_data, 'grossMargins'),

                # Dividen
                'dividend_yield': self.extract_value(summary_detail, 'dividendYield'),
                'dividend_rate': self.extract_value(summary_detail, 'dividendRate'),
                'payout_ratio': self.extract_value(summary_detail, 'payoutRatio'),

                # Valuasi
                'pe_ratio': self.extract_value(summary_detail, 'trailingPE'),
                'forward_pe': self.extract_value(summary_detail, 'forwardPE'),
                'pb_ratio': self.extract_value(summary_detail, 'priceToBook'),
                'peg_ratio': self.extract_value(key_stats, 'pegRatio'),

                # Likuiditas
                'current_ratio': self.extract_value(financial_data, 'currentRatio'),
                'quick_ratio': self.extract_value(financial_data, 'quickRatio'),

                # Pertumbuhan
                'earnings_growth': self.extract_value(financial_data, 'earningsGrowth'),
                'revenue_growth': self.extract_value(financial_data, 'revenueGrowth'),

                # Ukuran Perusahaan
                'market_cap': self.extract_value(price_data, 'marketCap'),
                'enterprise_value': self.extract_value(key_stats, 'enterpriseValue'),

                # EPS
                'eps': self.extract_value(key_stats, 'trailingEps'),
                'forward_eps': self.extract_value(key_stats, 'forwardEps'),
            }

            # Konversi persentase (nilai dari Yahoo Finance sudah dalam desimal 0-1)
            if data['roe'] is not None:
                data['roe'] = data['roe'] * 100  # Convert to percentage
            if data['roa'] is not None:
                data['roa'] = data['roa'] * 100
            if data['profit_margin'] is not None:
                data['profit_margin'] = data['profit_margin'] * 100
            if data['dividend_yield'] is not None:
                data['dividend_yield'] = data['dividend_yield'] * 100
            if data['earnings_growth'] is not None:
                data['earnings_growth'] = data['earnings_growth'] * 100
            if data['revenue_growth'] is not None:
                data['revenue_growth'] = data['revenue_growth'] * 100

            # D/E ratio dari Yahoo Finance kadang dalam persen
            if data['debt_to_equity'] is not None and data['debt_to_equity'] > 10:
                data['debt_to_equity'] = data['debt_to_equity'] / 100

            return data

        except Exception as e:
            print(f"    Error: {str(e)[:50]}")
            return None

    def fetch_all_stocks(self, tickers: List[str]) -> pd.DataFrame:
        """
        Mengambil data untuk semua saham dalam list

        Args:
            tickers: List kode saham

        Returns:
            DataFrame berisi semua data saham
        """
        all_data = []
        total = len(tickers)

        print(f"\n{'='*60}")
        print(f"  MENGAMBIL DATA {total} SAHAM IHSG")
        print(f"{'='*60}\n")

        for i, ticker in enumerate(tickers, 1):
            print(f"[{i}/{total}] Mengambil data {ticker}...", end=" ")

            data = self.get_stock_data(ticker)
            if data:
                all_data.append(data)
                print("OK")
            else:
                print("SKIP")

            # Delay untuk menghindari rate limiting
            time.sleep(1)

        df = pd.DataFrame(all_data)
        print(f"\n  Total saham berhasil diambil: {len(df)}/{total}")

        return df


def format_number(value, decimals=2, suffix=''):
    """Format angka untuk tampilan"""
    if value is None or pd.isna(value):
        return 'N/A'
    if suffix == 'T':
        return f"{value/1e12:.{decimals}f}T"
    elif suffix == 'B':
        return f"{value/1e9:.{decimals}f}B"
    elif suffix == 'M':
        return f"{value/1e6:.{decimals}f}M"
    elif suffix == '%':
        return f"{value:.{decimals}f}%"
    else:
        return f"{value:.{decimals}f}"
