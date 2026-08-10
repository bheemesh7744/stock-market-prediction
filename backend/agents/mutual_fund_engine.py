#!/usr/bin/env python3
"""
Mutual Funds Engine & Smart SIP Predictor
Provides NAV tracking, 1Y/3Y/5Y CAGR analytics, risk ratings, top holdings breakdown,
Pros & Cons analysis, AI Recommendation Rationale, and What-If-You-Buy outcome forecasting.
"""

import time
import math
import random
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger("MutualFundEngine")

TOP_MUTUAL_FUNDS = {
    "PPFCF": {
        "symbol": "PPFCF",
        "name": "Parag Parikh Flexi Cap Fund Direct Growth",
        "amc": "PPFAS Mutual Fund",
        "category": "Flexi Cap",
        "nav": 78.45,
        "prev_nav": 77.82,
        "cagr_1y": 24.8,
        "cagr_3y": 21.4,
        "cagr_5y": 23.2,
        "rating": 5,
        "aum": "₹68,500 Cr",
        "expense_ratio": 0.63,
        "risk": "Very High",
        "manager": "Rajeev Thakkar",
        "min_sip": 1000,
        "holdings": [
            {"stock": "RELIANCE", "name": "Reliance Industries", "weight": 8.4},
            {"stock": "HDFCBANK", "name": "HDFC Bank Ltd", "weight": 7.8},
            {"stock": "GOOGL", "name": "Alphabet Inc (US)", "weight": 6.2},
            {"stock": "ICICIBANK", "name": "ICICI Bank Ltd", "weight": 5.9},
            {"stock": "ITC", "name": "ITC Limited", "weight": 4.8}
        ],
        "why_recommendation": "Consistently outperforms NIFTY 50 by over +6% alpha with unique international equity diversification (US Tech exposure) and low downside capture ratio.",
        "pros": [
            "Consistent 20%+ 3Y CAGR outperforming NIFTY 50 benchmark",
            "International stock exposure (Alphabet/US Tech) provides USD currency hedge",
            "Competitive low expense ratio of 0.63% for active management"
        ],
        "cons": [
            "2% exit load if units redeemed within 1st year (1% in 2nd year)",
            "Large AUM size (₹68,500 Cr) limits agility in small-cap tactical moves"
        ],
        "what_happens_if_you_buy": {
            "short_term": "NAV moves steadily with Indian & US market indices. Moderate short-term price stability.",
            "long_term": "High probability of compounding wealth at ~21.4% CAGR. ₹1 Lakh invested 3 yrs ago is now ~₹1.78 Lakhs.",
            "action": "Strong Buy for 3+ year horizon via Monthly SIP or lump-sum dip buying."
        }
    },
    "QUANT_SMALL": {
        "symbol": "QUANT_SMALL",
        "name": "Quant Small Cap Fund Direct Growth",
        "amc": "Quant Mutual Fund",
        "category": "Small Cap",
        "nav": 245.12,
        "prev_nav": 242.30,
        "cagr_1y": 38.2,
        "cagr_3y": 32.1,
        "cagr_5y": 35.6,
        "rating": 5,
        "aum": "₹21,300 Cr",
        "expense_ratio": 0.77,
        "risk": "Very High",
        "manager": "Sandeep Tandon",
        "min_sip": 1000,
        "holdings": [
            {"stock": "RELIANCE", "name": "Reliance Industries", "weight": 9.1},
            {"stock": "GEOJIT", "name": "Geojit Financial", "weight": 5.4},
            {"stock": "IRB", "name": "IRB Infrastructure", "weight": 4.8},
            {"stock": "BIKAZI", "name": "Bikaji Foods", "weight": 4.1},
            {"stock": "JISLJALEQS", "name": "Jain Irrigation", "weight": 3.9}
        ],
        "why_recommendation": "Industry-leading 32.1% 3Y CAGR powered by Quant AMC's proprietary Predictive Analytics & VLRT momentum allocation model.",
        "pros": [
            "Top-performing small cap fund in India (32.1% 3Y CAGR)",
            "Dynamic asset allocation adapts rapidly to shifting economic cycles",
            "High upside alpha generation during Indian bull market rallies"
        ],
        "cons": [
            "Very high short-term volatility and Beta (> 1.15)",
            "Higher portfolio turnover ratio due to frequent algorithmic rebalancing"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Dynamic price swings. Expect temporary 10-15% drawdowns during broader market pullbacks.",
            "long_term": "Exceptional wealth multiplier. ₹1 Lakh invested 3 yrs ago grew to over ₹2.30 Lakhs.",
            "action": "Recommended for aggressive growth investors committed to a 3-5+ year holding period."
        }
    },
    "SBI_BLUE": {
        "symbol": "SBI_BLUE",
        "name": "SBI Bluechip Fund Direct Growth",
        "amc": "SBI Mutual Fund",
        "category": "Large Cap",
        "nav": 89.30,
        "prev_nav": 88.95,
        "cagr_1y": 19.5,
        "cagr_3y": 16.8,
        "cagr_5y": 17.4,
        "rating": 4,
        "aum": "₹46,200 Cr",
        "expense_ratio": 0.85,
        "risk": "Very High",
        "manager": "Sohini Andani",
        "min_sip": 500,
        "holdings": [
            {"stock": "ICICIBANK", "name": "ICICI Bank Ltd", "weight": 9.2},
            {"stock": "RELIANCE", "name": "Reliance Industries", "weight": 8.6},
            {"stock": "HDFCBANK", "name": "HDFC Bank Ltd", "weight": 8.1},
            {"stock": "INFY", "name": "Infosys Ltd", "weight": 5.8},
            {"stock": "LT", "name": "Larsen & Toubro", "weight": 5.1}
        ],
        "why_recommendation": "Stability-first large cap portfolio backed by India's largest AMC with proven 16.8% CAGR and low portfolio downside risk.",
        "pros": [
            "Heavy allocation to top India Inc market leaders (ICICI, Reliance, HDFC)",
            "Lower volatility profile compared to mid and small cap funds",
            "Proven 15+ year fund management track record"
        ],
        "cons": [
            "Returns closely track NIFTY 50 index (moderate alpha boost over index)",
            "Expense ratio of 0.85% is slightly higher than passive index funds"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Low price volatility with resilient capital preservation during market downturns.",
            "long_term": "Steady 16-18% wealth compounding. Provides baseline core portfolio stability.",
            "action": "Ideal foundational buy for conservative and first-time mutual fund investors."
        }
    },
    "MIRAE_LM": {
        "symbol": "MIRAE_LM",
        "name": "Mirae Asset Large & Midcap Fund Direct Growth",
        "amc": "Mirae Asset Mutual Fund",
        "category": "Large & MidCap",
        "nav": 132.60,
        "prev_nav": 131.90,
        "cagr_1y": 22.1,
        "cagr_3y": 19.5,
        "cagr_5y": 20.8,
        "rating": 4,
        "aum": "₹37,800 Cr",
        "expense_ratio": 0.61,
        "risk": "Very High",
        "manager": "Neelesh Surana",
        "min_sip": 1000,
        "holdings": [
            {"stock": "HDFCBANK", "name": "HDFC Bank Ltd", "weight": 6.8},
            {"stock": "ICICIBANK", "name": "ICICI Bank Ltd", "weight": 6.2},
            {"stock": "RELIANCE", "name": "Reliance Industries", "weight": 5.9},
            {"stock": "AXISBANK", "name": "Axis Bank Ltd", "weight": 4.2},
            {"stock": "BHARTIARTL", "name": "Bharti Airtel Ltd", "weight": 3.9}
        ],
        "why_recommendation": "Optimal blend of Large Cap stability (35%) and Mid Cap growth power (65%) delivering a strong 19.5% 3Y CAGR.",
        "pros": [
            "Balanced risk-reward ratio across large bluechips & mid-sized leaders",
            "Competitive direct plan expense ratio of 0.61%",
            "Consistently ranks in top performance quartile of Large & MidCap category"
        ],
        "cons": [
            "Mid-cap portion carries moderate volatility during market corrections",
            "1% exit load for unit redemptions within 1 year"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Moderate day-to-day price movement, outperforming pure large-caps during rallies.",
            "long_term": "Compounds wealth efficiently at 18-20% CAGR over a 3-5 year horizon.",
            "action": "Recommended for systematic wealth creation via monthly SIP."
        }
    },
    "HDFC_MID": {
        "symbol": "HDFC_MID",
        "name": "HDFC Mid-Cap Opportunities Fund Direct Growth",
        "amc": "HDFC Mutual Fund",
        "category": "Mid Cap",
        "nav": 175.20,
        "prev_nav": 173.80,
        "cagr_1y": 31.4,
        "cagr_3y": 27.8,
        "cagr_5y": 26.5,
        "rating": 5,
        "aum": "₹65,400 Cr",
        "expense_ratio": 0.74,
        "risk": "Very High",
        "manager": "Chirag Setalvad",
        "min_sip": 500,
        "holdings": [
            {"stock": "INDIANHOTE", "name": "Indian Hotels Co", "weight": 4.5},
            {"stock": "MAXHEALTH", "name": "Max Healthcare", "weight": 4.1},
            {"stock": "FEDERALBNK", "name": "Federal Bank Ltd", "weight": 3.8},
            {"stock": "COFORGE", "name": "Coforge Limited", "weight": 3.4},
            {"stock": "APOLLOTYRE", "name": "Apollo Tyres Ltd", "weight": 3.2}
        ],
        "why_recommendation": "Outstanding 27.8% 3Y CAGR managed by veteran Chirag Setalvad, capturing high-growth mid-cap market leaders early.",
        "pros": [
            "Outstanding 27.8% 3Y CAGR performance track record",
            "Proven stock-picking methodology in emerging mid-cap sector champions",
            "Low turnover ratio reflecting long-term conviction holding"
        ],
        "cons": [
            "Mid-cap sector subject to sharp pullbacks during broad market corrections",
            "Large AUM size (₹65,400 Cr) requires careful liquidity management"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Expect moderate-to-high volatility when broader market consolidates.",
            "long_term": "Aggressive wealth compounding. Multiplies invested capital every 3-4 years.",
            "action": "Strongly recommended for monthly SIP accumulation with 3+ year horizon."
        }
    },
    "NIPPON_SMALL": {
        "symbol": "NIPPON_SMALL",
        "name": "Nippon India Small Cap Fund Direct Growth",
        "amc": "Nippon India Mutual Fund",
        "category": "Small Cap",
        "nav": 182.40,
        "prev_nav": 180.10,
        "cagr_1y": 41.2,
        "cagr_3y": 34.5,
        "cagr_5y": 33.1,
        "rating": 5,
        "aum": "₹52,900 Cr",
        "expense_ratio": 0.67,
        "risk": "Very High",
        "manager": "Samir Rachh",
        "min_sip": 100,
        "holdings": [
            {"stock": "TUBEINVEST", "name": "Tube Investments", "weight": 3.2},
            {"stock": "HDFC_BANK", "name": "HDFC Bank Ltd", "weight": 2.9},
            {"stock": "KPITTECH", "name": "KPIT Technologies", "weight": 2.7},
            {"stock": "APARINDS", "name": "Apar Industries Ltd", "weight": 2.5},
            {"stock": "MULTIOPT", "name": "Multi Commodity Exch", "weight": 2.4}
        ],
        "why_recommendation": "Phenomenal 34.5% 3Y CAGR with deep research coverage across 150+ small-cap growth champions mitigating individual stock risk.",
        "pros": [
            "Massive multi-bagger return potential in small-cap growth leaders",
            "Broadly diversified portfolio (150+ stocks reduces single-stock risk)",
            "Industry-leading 5-year CAGR of 33.1%"
        ],
        "cons": [
            "High short-term price volatility during small-cap index pullbacks",
            "Lump-sum investments occasionally restricted by AMC due to high AUM inflows"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Price moves dynamically with small-cap market sentiment.",
            "long_term": "Highest wealth creation potential among equity funds. Transforms small SIPs into significant capital.",
            "action": "Must-have for long-term aggressive growth portfolios via monthly SIP."
        }
    },
    "TATA_DIGITAL": {
        "symbol": "TATA_DIGITAL",
        "name": "Tata Digital India Fund Direct Growth",
        "amc": "Tata Mutual Fund",
        "category": "Sectoral / IT",
        "nav": 48.90,
        "prev_nav": 48.35,
        "cagr_1y": 26.5,
        "cagr_3y": 18.2,
        "cagr_5y": 24.1,
        "rating": 4,
        "aum": "₹9,800 Cr",
        "expense_ratio": 0.34,
        "risk": "Very High",
        "manager": "Meeta Shetty",
        "min_sip": 150,
        "holdings": [
            {"stock": "TCS", "name": "Tata Consultancy Svcs", "weight": 19.8},
            {"stock": "INFY", "name": "Infosys Ltd", "weight": 18.2},
            {"stock": "HCLTECH", "name": "HCL Technologies", "weight": 9.4},
            {"stock": "TECHM", "name": "Tech Mahindra Ltd", "weight": 7.1},
            {"stock": "WIPRO", "name": "Wipro Limited", "weight": 5.8}
        ],
        "why_recommendation": "Focused play on India's top IT & Digital leaders (TCS, Infosys, HCL) benefiting from global AI, Cloud & Enterprise tech expansion.",
        "pros": [
            "Ultra-low direct expense ratio of 0.34%",
            "Direct exposure to cash-rich Indian IT giants and global AI trends",
            "Strong 26.5% 1-year return rebound"
        ],
        "cons": [
            "High sector concentration risk (100% technology sector exposure)",
            "Vulnerable to US tech spending cutbacks and USD/INR currency shifts"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Tightly correlated with NASDAQ & NIFTY IT index earnings reports.",
            "long_term": "Rides global digital transformation and AI technology boom over 3-5 years.",
            "action": "Recommended as a tactical 10-15% sector allocation in your portfolio."
        }
    },
    "ICICI_TECH": {
        "symbol": "ICICI_TECH",
        "name": "ICICI Prudential Technology Fund Direct Growth",
        "amc": "ICICI Prudential Mutual Fund",
        "category": "Sectoral / IT",
        "nav": 195.80,
        "prev_nav": 193.90,
        "cagr_1y": 25.1,
        "cagr_3y": 17.9,
        "cagr_5y": 23.8,
        "rating": 4,
        "aum": "₹12,400 Cr",
        "expense_ratio": 0.88,
        "risk": "Very High",
        "manager": "Vaibhav Dusad",
        "min_sip": 100,
        "holdings": [
            {"stock": "INFY", "name": "Infosys Ltd", "weight": 21.5},
            {"stock": "TCS", "name": "Tata Consultancy Svcs", "weight": 17.4},
            {"stock": "BHARTIARTL", "name": "Bharti Airtel Ltd", "weight": 8.9},
            {"stock": "HCLTECH", "name": "HCL Technologies", "weight": 7.8},
            {"stock": "PERSISTENT", "name": "Persistent Systems", "weight": 5.2}
        ],
        "why_recommendation": "Riding tech sector recovery with 25.1% 1Y returns and strong concentration in top dividend-paying IT exporters.",
        "pros": [
            "High upside potential as global corporate IT budgets recover",
            "Top IT holdings (Infosys, TCS) generate heavy dividend cash flows",
            "Strong 5Y CAGR of 23.8%"
        ],
        "cons": [
            "Single-sector risk (IT & Telecom only)",
            "Higher expense ratio (0.88%) compared to passive IT index funds"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Correlated with IT sector quarterly earnings and US tech sentiment.",
            "long_term": "Solid tech growth play delivering high returns during IT bull cycles.",
            "action": "Good tactical buy during IT sector dips for growth-oriented portfolios."
        }
    },
    "AXIS_ELSS": {
        "symbol": "AXIS_ELSS",
        "name": "Axis Long Term Equity Fund Direct Growth (ELSS)",
        "amc": "Axis Mutual Fund",
        "category": "ELSS / Tax Saver",
        "nav": 94.10,
        "prev_nav": 93.65,
        "cagr_1y": 17.2,
        "cagr_3y": 14.5,
        "cagr_5y": 15.8,
        "rating": 4,
        "aum": "₹28,600 Cr",
        "expense_ratio": 0.72,
        "risk": "High",
        "manager": "Jinesh Gopani",
        "min_sip": 500,
        "holdings": [
            {"stock": "BAJFINANCE", "name": "Bajaj Finance Ltd", "weight": 8.1},
            {"stock": "AvenueSupermarts", "name": "Avenue Supermarts", "weight": 7.4},
            {"stock": "ICICIBANK", "name": "ICICI Bank Ltd", "weight": 6.8},
            {"stock": "TCS", "name": "Tata Consultancy Svcs", "weight": 5.9},
            {"stock": "HDFCBANK", "name": "HDFC Bank Ltd", "weight": 5.2}
        ],
        "why_recommendation": "Dual benefit of Section 80C Tax Saving (up to ₹1.5 Lakh tax deduction) plus steady 14.5% equity compounding.",
        "pros": [
            "Saves up to ₹46,800 in income tax per year under Section 80C",
            "3-year mandatory lock-in prevents emotional panic selling",
            "Quality growth stock selection (Bajaj Finance, ICICI Bank)"
        ],
        "cons": [
            "Mandatory 3-year lock-in period (units cannot be redeemed before 36 months)",
            "Moderate returns compared to non-ELSS small/mid-cap funds"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Funds are locked for 3 years, insulating your capital from short-term market noise.",
            "long_term": "Combines immediate tax savings with compounding equity wealth over 3+ years.",
            "action": "Best choice for salaried professionals seeking tax savings + equity growth."
        }
    },
    "UTI_NIFTY50": {
        "symbol": "UTI_NIFTY50",
        "name": "UTI Nifty 50 Index Fund Direct Growth",
        "amc": "UTI Mutual Fund",
        "category": "Index Fund",
        "nav": 162.30,
        "prev_nav": 161.40,
        "cagr_1y": 18.4,
        "cagr_3y": 15.8,
        "cagr_5y": 16.4,
        "rating": 5,
        "aum": "₹16,900 Cr",
        "expense_ratio": 0.21,
        "risk": "High",
        "manager": "Sharwan Kumar Goyal",
        "min_sip": 500,
        "holdings": [
            {"stock": "HDFCBANK", "name": "HDFC Bank Ltd", "weight": 11.4},
            {"stock": "RELIANCE", "name": "Reliance Industries", "weight": 9.8},
            {"stock": "ICICIBANK", "name": "ICICI Bank Ltd", "weight": 7.9},
            {"stock": "INFY", "name": "Infosys Ltd", "weight": 5.7},
            {"stock": "ITC", "name": "ITC Limited", "weight": 4.3}
        ],
        "why_recommendation": "Lowest expense ratio (0.21%) passive index fund replicating top 50 bluechips of India with zero fund manager bias.",
        "pros": [
            "Ultra-low expense ratio (0.21%) maximizing net investor returns",
            "Zero fund manager risk (100% passive tracking of NIFTY 50 index)",
            "Guaranteed market returns with near-zero tracking error"
        ],
        "cons": [
            "Will never beat the market index (gives exact market return)",
            "No downside cash protection during broad market crashes"
        ],
        "what_happens_if_you_buy": {
            "short_term": "Mirrors the exact movement of NIFTY 50 index daily.",
            "long_term": "Safest equity wealth builder. Historically doubles capital every 5-6 years (~15-16% CAGR).",
            "action": "Highly recommended foundational buy for all investors seeking low-cost market returns."
        }
    }
}

def get_live_nav_info(fund_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate live NAV with small intraday fluctuation, return %, and AI signals."""
    base_nav = fund_data["nav"]
    prev_nav = fund_data["prev_nav"]
    
    # Introduce micro noise based on current time for realistic live updating
    seed = int(time.time() // 15) + hash(fund_data["symbol"])
    random.seed(seed)
    micro_offset = (random.random() - 0.48) * (base_nav * 0.003)
    
    current_nav = round(base_nav + micro_offset, 2)
    nav_change = round(current_nav - prev_nav, 2)
    nav_change_pct = round((nav_change / prev_nav) * 100, 2)
    
    # Determine AI Signal & Score based on CAGR & volatility
    cagr3 = fund_data["cagr_3y"]
    if cagr3 >= 30.0:
        signal = "STRONG BUY"
        signal_color = "emerald"
        ai_score = round(92 + (cagr3 - 30) * 0.5, 1)
    elif cagr3 >= 20.0:
        signal = "BUY"
        signal_color = "teal"
        ai_score = round(84 + (cagr3 - 20) * 0.8, 1)
    elif cagr3 >= 15.0:
        signal = "ACCUMULATE SIP"
        signal_color = "blue"
        ai_score = round(76 + (cagr3 - 15) * 1.2, 1)
    else:
        signal = "HOLD"
        signal_color = "amber"
        ai_score = round(68 + (cagr3 - 10) * 1.0, 1)
        
    ai_score = min(99.0, max(50.0, ai_score))
    
    return {
        "symbol": fund_data["symbol"],
        "name": fund_data["name"],
        "amc": fund_data["amc"],
        "category": fund_data["category"],
        "nav": current_nav,
        "prev_nav": prev_nav,
        "nav_change": nav_change,
        "nav_change_pct": nav_change_pct,
        "cagr_1y": fund_data["cagr_1y"],
        "cagr_3y": fund_data["cagr_3y"],
        "cagr_5y": fund_data["cagr_5y"],
        "rating": fund_data["rating"],
        "aum": fund_data["aum"],
        "expense_ratio": fund_data["expense_ratio"],
        "risk": fund_data["risk"],
        "manager": fund_data["manager"],
        "min_sip": fund_data["min_sip"],
        "holdings": fund_data["holdings"],
        "why_recommendation": fund_data.get("why_recommendation", ""),
        "pros": fund_data.get("pros", []),
        "cons": fund_data.get("cons", []),
        "what_happens_if_you_buy": fund_data.get("what_happens_if_you_buy", {}),
        "ai_signal": signal,
        "ai_signal_color": signal_color,
        "ai_score": ai_score,
    }


def get_all_mutual_funds(category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return all mutual funds, optionally filtered by category."""
    results = []
    for sym, fund in TOP_MUTUAL_FUNDS.items():
        if category_filter and category_filter.lower() != 'all':
            cat = fund["category"].lower()
            filt = category_filter.lower()
            if filt not in cat and cat not in filt:
                continue
        results.append(get_live_nav_info(fund))
    return results


def get_mutual_fund_detail(symbol: str) -> Optional[Dict[str, Any]]:
    """Return detailed analytics for a single mutual fund."""
    if symbol not in TOP_MUTUAL_FUNDS:
        return None
    
    fund = TOP_MUTUAL_FUNDS[symbol]
    live_info = get_live_nav_info(fund)
    
    # Generate historical NAV curve (180 days)
    nav_history = []
    base_price = live_info["nav"]
    cagr = fund["cagr_1y"] / 100.0
    daily_growth = math.pow(1 + cagr, 1 / 365.0)
    
    random.seed(42 + hash(symbol))
    curr = base_price * 0.75  # 180 days ago NAV
    for day in range(180, 0, -1):
        noise = (random.random() - 0.47) * (curr * 0.012)
        curr = curr * daily_growth + noise
        nav_history.append({"day": 181 - day, "nav": round(curr, 2)})
    
    nav_history[-1]["nav"] = live_info["nav"]
    
    # SIP Calculator simulation (₹5,000 / month for 3 years)
    monthly_investment = 5000
    months = 36
    total_invested = monthly_investment * months
    monthly_rate = (fund["cagr_3y"] / 100.0) / 12.0
    
    future_val = monthly_investment * (((math.pow(1 + monthly_rate, months) - 1) / monthly_rate) * (1 + monthly_rate))
    total_returns = future_val - total_invested
    
    live_info["history"] = nav_history
    live_info["sip_analysis"] = {
        "monthly_amount": monthly_investment,
        "duration_years": 3,
        "total_invested": round(total_invested, 2),
        "projected_value": round(future_val, 2),
        "total_returns": round(total_returns, 2),
        "absolute_return_pct": round((total_returns / total_invested) * 100, 2)
    }
    
    return live_info


def predict_mutual_fund_nav(symbol: str) -> Optional[Dict[str, Any]]:
    """Generate 30d, 90d, and 1y AI NAV projections and Smart SIP buy recommendations."""
    if symbol not in TOP_MUTUAL_FUNDS:
        return None
    
    fund = TOP_MUTUAL_FUNDS[symbol]
    live_info = get_live_nav_info(fund)
    current_nav = live_info["nav"]
    cagr3 = fund["cagr_3y"] / 100.0
    
    target_30d = round(current_nav * math.pow(1 + cagr3, 30 / 365.0), 2)
    target_90d = round(current_nav * math.pow(1 + cagr3, 90 / 365.0), 2)
    target_1y = round(current_nav * (1 + cagr3), 2)
    
    return {
        "symbol": symbol,
        "name": fund["name"],
        "current_nav": current_nav,
        "projected_targets": {
            "30_days": {"nav": target_30d, "gain_pct": round(((target_30d - current_nav) / current_nav) * 100, 2)},
            "90_days": {"nav": target_90d, "gain_pct": round(((target_90d - current_nav) / current_nav) * 100, 2)},
            "1_year": {"nav": target_1y, "gain_pct": round(cagr3 * 100, 2)}
        },
        "smart_sip_insights": {
            "optimal_buy_date": "5th of every month (Post salary credit)",
            "dip_buying_opportunity": "ACTIVE" if live_info["nav_change_pct"] < 0 else "NORMAL ACCUMULATION",
            "alpha_forecast": f"+{round(cagr3 * 100 - 15.0, 1)}% over NIFTY 50 benchmark",
            "top_stock_catalysts": [h["name"] for h in fund["holdings"][:3]]
        },
        "why_recommendation": live_info["why_recommendation"],
        "pros": live_info["pros"],
        "cons": live_info["cons"],
        "what_happens_if_you_buy": live_info["what_happens_if_you_buy"],
        "ai_signal": live_info["ai_signal"],
        "ai_score": live_info["ai_score"]
    }
