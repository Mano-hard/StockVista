import yfinance as yf
import pandas as pd
import requests
import json
from typing import List, Dict, Optional, Tuple

class CompanySearcher:
    def __init__(self):
        # Common Indian stock exchanges
        self.indian_exchanges = ['.NS', '.BO']  # NSE and BSE
        
        # Major Indian companies mapping (name to symbol)
        self.indian_companies = {
            # Technology
            'tcs': 'TCS.NS',
            'tata consultancy services': 'TCS.NS',
            'infosys': 'INFY.NS',
            'wipro': 'WIPRO.NS',
            'hcl technologies': 'HCLTECH.NS',
            'tech mahindra': 'TECHM.NS',
            
            # Banking & Finance
            'hdfc bank': 'HDFCBANK.NS',
            'icici bank': 'ICICIBANK.NS',
            'state bank of india': 'SBIN.NS',
            'sbi': 'SBIN.NS',
            'axis bank': 'AXISBANK.NS',
            'kotak mahindra bank': 'KOTAKBANK.NS',
            'bajaj finance': 'BAJFINANCE.NS',
            'hdfc': 'HDFC.NS',
            
            # Automotive
            'tata motors': 'TATAMOTORS.NS',
            'maruti suzuki': 'MARUTI.NS',
            'mahindra': 'M&M.NS',
            'bajaj auto': 'BAJAJ-AUTO.NS',
            'hero motocorp': 'HEROMOTOCO.NS',
            'tvs motor': 'TVSMOTOR.NS',
            
            # Pharmaceuticals
            'sun pharma': 'SUNPHARMA.NS',
            'dr reddy': 'DRREDDY.NS',
            'cipla': 'CIPLA.NS',
            'lupin': 'LUPIN.NS',
            'aurobindo pharma': 'AUROPHARMA.NS',
            'divi\'s laboratories': 'DIVISLAB.NS',
            
            # Oil & Gas
            'reliance': 'RELIANCE.NS',
            'reliance industries': 'RELIANCE.NS',
            'oil and natural gas corporation': 'ONGC.NS',
            'ongc': 'ONGC.NS',
            'indian oil': 'IOC.NS',
            'bharat petroleum': 'BPCL.NS',
            'hindustan petroleum': 'HINDPETRO.NS',
            
            # Metals & Mining
            'tata steel': 'TATASTEEL.NS',
            'jsw steel': 'JSWSTEEL.NS',
            'hindalco': 'HINDALCO.NS',
            'vedanta': 'VEDL.NS',
            'coal india': 'COALINDIA.NS',
            'nmdc': 'NMDC.NS',
            
            # Consumer Goods
            'hindustan unilever': 'HINDUNILVR.NS',
            'hul': 'HINDUNILVR.NS',
            'itc': 'ITC.NS',
            'nestle india': 'NESTLEIND.NS',
            'britannia': 'BRITANNIA.NS',
            'godrej consumer': 'GODREJCP.NS',
            
            # Telecom
            'bharti airtel': 'BHARTIARTL.NS',
            'airtel': 'BHARTIARTL.NS',
            'vodafone idea': 'IDEA.NS',
            'jio': 'RJIO.NS',
            
            # Power & Infrastructure
            'ntpc': 'NTPC.NS',
            'power grid': 'POWERGRID.NS',
            'larsen toubro': 'LT.NS',
            'l&t': 'LT.NS',
            'ultratech cement': 'ULTRACEMCO.NS',
            'grasim': 'GRASIM.NS',
            
            # Others
            'adani enterprises': 'ADANIENT.NS',
            'asian paints': 'ASIANPAINT.NS',
            'bajaj finserv': 'BAJAJFINSV.NS',
            'titan': 'TITAN.NS',
            'wipro': 'WIPRO.NS'
        }
        
        # US companies mapping (name to symbol)
        self.us_companies = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'nvidia': 'NVDA',
            'intel': 'INTC',
            'amd': 'AMD',
            'oracle': 'ORCL',
            'salesforce': 'CRM',
            'adobe': 'ADBE',
            'paypal': 'PYPL',
            'visa': 'V',
            'mastercard': 'MA',
            'jpmorgan': 'JPM',
            'jp morgan': 'JPM',
            'bank of america': 'BAC',
            'wells fargo': 'WFC',
            'goldman sachs': 'GS',
            'morgan stanley': 'MS',
            'berkshire hathaway': 'BRK-B',
            'johnson & johnson': 'JNJ',
            'pfizer': 'PFE',
            'coca cola': 'KO',
            'pepsi': 'PEP',
            'walmart': 'WMT',
            'home depot': 'HD',
            'disney': 'DIS',
            'boeing': 'BA',
            'caterpillar': 'CAT',
            'exxon mobil': 'XOM',
            'chevron': 'CVX'
        }
    
    def search_company(self, query: str) -> Optional[str]:
        """
        Search for a company by name or symbol and return the appropriate ticker symbol
        """
        query_lower = query.lower().strip()
        
        # First check if it's already a valid symbol
        if self._is_valid_symbol(query.upper()):
            return query.upper()
        
        # Check Indian companies
        if query_lower in self.indian_companies:
            return self.indian_companies[query_lower]
        
        # Check US companies
        if query_lower in self.us_companies:
            return self.us_companies[query_lower]
        
        # Try partial matching for Indian companies
        for name, symbol in self.indian_companies.items():
            if query_lower in name or name in query_lower:
                return symbol
        
        # Try partial matching for US companies
        for name, symbol in self.us_companies.items():
            if query_lower in name or name in query_lower:
                return symbol
        
        # Try with Indian exchange suffixes
        for exchange in self.indian_exchanges:
            test_symbol = f"{query.upper()}{exchange}"
            if self._is_valid_symbol(test_symbol):
                return test_symbol
        
        # If nothing found, return the original query (let yfinance handle it)
        return query.upper()
    
    def _is_valid_symbol(self, symbol: str) -> bool:
        """
        Check if a symbol is valid by attempting to fetch basic info
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return bool(info and 'symbol' in info)
        except:
            return False
    
    def get_suggestions(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Get suggestions for company names based on partial query
        """
        query_lower = query.lower().strip()
        suggestions = []
        
        # Search Indian companies
        for name, symbol in self.indian_companies.items():
            if query_lower in name and len(suggestions) < limit:
                suggestions.append({
                    'name': name.title(),
                    'symbol': symbol,
                    'exchange': 'India (NSE/BSE)'
                })
        
        # Search US companies
        for name, symbol in self.us_companies.items():
            if query_lower in name and len(suggestions) < limit:
                suggestions.append({
                    'name': name.title(),
                    'symbol': symbol,
                    'exchange': 'US (NASDAQ/NYSE)'
                })
        
        return suggestions[:limit]

class ProfitCompoundingAnalyzer:
    def __init__(self):
        pass
    
    def analyze_profit_compounding(self, ticker, info) -> Dict:
        """
        Analyze whether the company is compounding its profits effectively
        """
        try:
            # Get financial data
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            
            if financials.empty:
                return self._get_fallback_analysis()
            
            analysis = {
                'is_compounding': False,
                'compounding_score': 0,
                'revenue_growth': None,
                'profit_growth': None,
                'roe_trend': None,
                'retained_earnings_growth': None,
                'debt_management': None,
                'efficiency_metrics': {},
                'compounding_factors': [],
                'warnings': []
            }
            
            # 1. Revenue Growth Analysis
            if 'Total Revenue' in financials.index:
                revenues = financials.loc['Total Revenue'].dropna()
                if len(revenues) >= 3:
                    revenue_growth_rates = revenues.pct_change().dropna()
                    avg_revenue_growth = revenue_growth_rates.mean()
                    analysis['revenue_growth'] = avg_revenue_growth * 100
                    
                    if avg_revenue_growth > 0.05:  # >5% average growth
                        analysis['compounding_score'] += 2
                        analysis['compounding_factors'].append(f"Strong revenue growth ({avg_revenue_growth*100:.1f}% avg)")
                    elif avg_revenue_growth > 0:
                        analysis['compounding_score'] += 1
                        analysis['compounding_factors'].append("Positive revenue growth")
                    else:
                        analysis['warnings'].append("Declining revenue trend")
            
            # 2. Net Income Growth Analysis
            net_income_keys = ['Net Income', 'Net Income Common Stockholders', 'Net Income Applicable To Common Shares']
            net_income = None
            
            for key in net_income_keys:
                if key in financials.index:
                    net_income = financials.loc[key].dropna()
                    break
            
            if net_income is not None and len(net_income) >= 3:
                profit_growth_rates = net_income.pct_change().dropna()
                avg_profit_growth = profit_growth_rates.mean()
                analysis['profit_growth'] = avg_profit_growth * 100
                
                if avg_profit_growth > 0.10:  # >10% average growth
                    analysis['compounding_score'] += 3
                    analysis['compounding_factors'].append(f"Excellent profit growth ({avg_profit_growth*100:.1f}% avg)")
                elif avg_profit_growth > 0.05:
                    analysis['compounding_score'] += 2
                    analysis['compounding_factors'].append("Good profit growth")
                elif avg_profit_growth > 0:
                    analysis['compounding_score'] += 1
                    analysis['compounding_factors'].append("Moderate profit growth")
                else:
                    analysis['warnings'].append("Declining profitability")
            
            # 3. Return on Equity (ROE) Analysis
            if not balance_sheet.empty:
                try:
                    # Calculate ROE for multiple years
                    stockholder_equity_keys = ['Stockholders Equity', 'Total Stockholder Equity', 'Total Equity']
                    stockholder_equity = None
                    
                    for key in stockholder_equity_keys:
                        if key in balance_sheet.index:
                            stockholder_equity = balance_sheet.loc[key].dropna()
                            break
                    
                    if stockholder_equity is not None and net_income is not None:
                        # Align dates
                        common_dates = stockholder_equity.index.intersection(net_income.index)
                        if len(common_dates) >= 2:
                            roe_values = []
                            for date in common_dates:
                                if stockholder_equity[date] > 0:
                                    roe = (net_income[date] / stockholder_equity[date]) * 100
                                    roe_values.append(roe)
                            
                            if roe_values:
                                avg_roe = sum(roe_values) / len(roe_values)
                                analysis['roe_trend'] = avg_roe
                                
                                if avg_roe > 15:  # >15% ROE
                                    analysis['compounding_score'] += 2
                                    analysis['compounding_factors'].append(f"High ROE ({avg_roe:.1f}%)")
                                elif avg_roe > 10:
                                    analysis['compounding_score'] += 1
                                    analysis['compounding_factors'].append("Good ROE")
                                elif avg_roe < 5:
                                    analysis['warnings'].append("Low return on equity")
                except:
                    pass
            
            # 4. Retained Earnings Analysis
            if not balance_sheet.empty:
                try:
                    retained_earnings_keys = ['Retained Earnings', 'Accumulated Retained Earnings']
                    for key in retained_earnings_keys:
                        if key in balance_sheet.index:
                            retained_earnings = balance_sheet.loc[key].dropna()
                            if len(retained_earnings) >= 3:
                                re_growth_rates = retained_earnings.pct_change().dropna()
                                avg_re_growth = re_growth_rates.mean()
                                analysis['retained_earnings_growth'] = avg_re_growth * 100
                                
                                if avg_re_growth > 0.05:
                                    analysis['compounding_score'] += 1
                                    analysis['compounding_factors'].append("Growing retained earnings")
                                elif avg_re_growth < 0:
                                    analysis['warnings'].append("Declining retained earnings")
                            break
                except:
                    pass
            
            # 5. Debt Management
            debt_to_equity = info.get('debtToEquity', 0)
            if debt_to_equity:
                analysis['debt_management'] = debt_to_equity
                if debt_to_equity < 0.3:  # Low debt
                    analysis['compounding_score'] += 1
                    analysis['compounding_factors'].append("Conservative debt management")
                elif debt_to_equity > 1.0:  # High debt
                    analysis['warnings'].append("High debt levels may limit growth")
            
            # 6. Efficiency Metrics
            profit_margin = info.get('profitMargins', 0)
            if profit_margin:
                analysis['efficiency_metrics']['profit_margin'] = profit_margin * 100
                if profit_margin > 0.15:  # >15% margin
                    analysis['compounding_score'] += 1
                    analysis['compounding_factors'].append("High profit margins")
            
            # 7. Determine if company is compounding
            if analysis['compounding_score'] >= 5:
                analysis['is_compounding'] = True
            
            return analysis
            
        except Exception as e:
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self):
        """Return basic analysis when data is insufficient"""
        return {
            'is_compounding': None,
            'compounding_score': 0,
            'revenue_growth': None,
            'profit_growth': None,
            'roe_trend': None,
            'retained_earnings_growth': None,
            'debt_management': None,
            'efficiency_metrics': {},
            'compounding_factors': [],
            'warnings': ['Insufficient financial data for compounding analysis']
        }
    
    def get_compounding_recommendation(self, analysis: Dict) -> str:
        """
        Generate recommendation based on compounding analysis
        """
        if analysis['is_compounding'] is None:
            return "Unable to determine compounding quality due to insufficient data"
        
        if analysis['is_compounding']:
            return "Strong compounding characteristics - company effectively reinvests profits for growth"
        elif analysis['compounding_score'] >= 3:
            return "Moderate compounding potential - some positive indicators but room for improvement"
        else:
            return "Weak compounding profile - limited evidence of effective profit reinvestment"