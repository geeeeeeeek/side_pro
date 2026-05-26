import akshare as ak
import requests
import pandas as pd
import numpy as np
import time
import warnings
from datetime import datetime

import constants

warnings.filterwarnings('ignore')

# 多因子美股预测方法
class MultiFactorStockScorer:
    def __init__(self, ticker: str, av_api_key: str):
        self.ticker = ticker.upper()
        self.av_api_key = av_api_key
        self.data = None
        self.scores = {}
        self.final_score = None
        self.fundamentals = None  # 保存基本面原始数据

    def fetch_data(self, start_date="20230101"):
        """AKShare 获取K线"""
        try:
            print(f"正在获取 {self.ticker} K线数据...")
            df = ak.stock_us_daily(symbol=self.ticker, adjust="qfq")
            df = df[df['date'] >= start_date].copy()
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

            self.data = df
            print(f"✅ K线获取成功 | 最新价: ${df['close'].iloc[-1]:.2f}")
            return True
        except Exception as e:
            print(f"❌ K线获取失败: {e}")
            return False

    def get_fundamentals(self):
        """Alpha Vantage 获取基本面数据（OVERVIEW）"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "OVERVIEW",
                "symbol": self.ticker,
                "apikey": self.av_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            print('基本面数据-->', data)

            if "Symbol" not in data:
                print("⚠️ 基本面数据获取失败，使用默认值")
                self.fundamentals = {}
                return {}

            self.fundamentals = data
            print(f"✅ 基本面数据获取成功 | MarketCap: ${float(data.get('MarketCapitalization', 0)) / 1e9:.1f}B")
            return data
        except Exception as e:
            print(f"❌ 基本面获取异常: {e}")
            self.fundamentals = {}
            return {}

    def fundamental_factors(self) -> float:
        """基本面得分（0-100）"""
        if not self.fundamentals:
            self.get_fundamentals()

        info = self.fundamentals
        score = 50.0

        # 1. 估值得分 (PE)
        try:
            pe = float(info.get('PERatio', 25) or 25)
            if pe < 18:
                score += 22
            elif pe < 28:
                score += 10
            elif pe > 45:
                score -= 20
        except:
            pass

        # 2. 盈利能力 (ROE)
        try:
            roe = float(info.get('ReturnOnEquityTTM', 0.1) or 0.1)
            if roe > 0.20:
                score += 18
            elif roe > 0.12:
                score += 8
            elif roe < 0.05:
                score -= 15
        except:
            pass

        # 3. 成长性 (EPS增长)
        try:
            eps_growth = float(info.get('EPSGrowthThisYear', 0) or 0)
            if eps_growth > 0.25:
                score += 15
            elif eps_growth > 0.10:
                score += 8
        except:
            pass

        # 4. 市值规模（大公司相对稳定）
        try:
            mkt_cap = float(info.get('MarketCapitalization', 0) or 0)
            if mkt_cap > 200000000000:  # > 2000亿
                score += 8
        except:
            pass

        final_fund_score = round(min(max(score, 15), 95), 1)
        self.scores['fundamental'] = final_fund_score
        return final_fund_score

    def get_sentiment_score(self, limit=8):
        """Alpha Vantage 新闻情绪"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": self.ticker,
                "limit": limit,
                "apikey": self.av_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            print('resp-->', data)

            if "feed" not in data:
                self.scores['sentiment'] = 55.0
                return 55.0

            total_score = 0
            count = 0

            for item in data["feed"][:limit]:
                score = item.get("overall_sentiment_score", 0)
                total_score += score
                count += 1

            avg_score = total_score / count if count > 0 else 0
            sentiment_score = round(50 + avg_score * 50, 1)  # 转为0-100
            self.scores['sentiment'] = sentiment_score
            return sentiment_score
        except:
            self.scores['sentiment'] = 55.0
            return 55.0

    def technical_factors(self) -> float:
        """技术面（保持不变）"""
        if self.data is None or len(self.data) < 50:
            self.scores['technical'] = 50.0
            return 50.0

        close = self.data['close']
        price = close.iloc[-1]

        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]
        ma200 = close.rolling(200).mean().iloc[-1] if len(close) >= 200 else ma50

        if price > ma20 > ma50 > ma200:
            trend = 90
        elif price > ma20 > ma50:
            trend = 75
        elif price < ma20 < ma50:
            trend = 30
        else:
            trend = 20

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean().iloc[-1]
        loss = -delta.where(delta < 0, 0).rolling(14).mean().iloc[-1]
        rsi = 50 if loss == 0 else 100 - (100 / (1 + gain / loss))

        tech_score = round(trend * 0.6 + (80 if 40 < rsi < 70 else 35) * 0.4, 1)
        self.scores['technical'] = tech_score
        return tech_score

    def momentum_volume_factors(self) -> float:
        """量价动量（保持不变）"""
        if self.data is None or len(self.data) < 20:
            self.scores['momentum'] = 50.0
            return 50.0

        df = self.data
        ret_5 = (df['close'].iloc[-1] / df['close'].iloc[-5] - 1) * 100
        ret_20 = (df['close'].iloc[-1] / df['close'].iloc[-20] - 1) * 100

        vol_ma = df['volume'].rolling(20).mean().iloc[-1]
        vol_ratio = df['volume'].iloc[-1] / vol_ma if vol_ma > 0 else 1

        score = 50
        if vol_ratio > 1.5 and ret_5 > 0: score += 22
        if ret_20 > 10:
            score += 18
        elif ret_20 < -15:
            score -= 20

        self.scores['momentum'] = round(min(max(score, 10), 95), 1)
        return self.scores['momentum']

    def calculate_final_score(self):
        """综合加权打分"""
        weights = {
            'technical': 0.30,
            'fundamental': 0.35,
            'momentum': 0.20,
            'sentiment': 0.15
        }

        self.technical_factors()
        self.fundamental_factors()
        self.momentum_volume_factors()
        self.get_sentiment_score(limit=8)

        self.final_score = round(
            sum(self.scores.get(k, 50) * weights.get(k, 0) for k in weights), 1
        )
        return self.final_score

    def generate_report(self):
        print("\n" + "=" * 80)
        print(f"             {self.ticker} 多因子综合评分报告（含基本面）")
        print("=" * 80)
        print(f"最新收盘价 : ${self.data['close'].iloc[-1]:.2f}")
        for k, v in self.scores.items():
            print(f"{k.capitalize():12} : {v:6.1f} 分")
        print("-" * 65)
        print(f"【最终综合得分】: {self.final_score} / 100\n")

        if self.final_score >= 78:
            print("强烈推荐 - 技术+基本面+情绪共振")
        elif self.final_score >= 65:
            print("值得重点关注")
        elif self.final_score >= 48:
            print("中性观望")
        else:
            print("建议回避")


# ====================== 使用 ======================
if __name__ == "__main__":
    AV_API_KEY = constants.API_KEY  # 改成自己的key 申请地址：https://www.alphavantage.co/

    tickers = ["TSLA"]

    for ticker in tickers:
        print(f"\n开始分析 {ticker} ...")
        scorer = MultiFactorStockScorer(ticker, AV_API_KEY)

        if scorer.fetch_data(start_date="20230101"):
            scorer.calculate_final_score()
            scorer.generate_report()
            time.sleep(15)
