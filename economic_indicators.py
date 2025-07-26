import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fredapi import Fred
import yfinance as yf

class EconomicAnalyzer:
    def __init__(self):
        # Initialize FRED API (Federal Reserve Economic Data)
        # Note: For production, you should get a FRED API key
        self.fred = None
        try:
            # Try to initialize FRED - will work without API key for basic data
            self.fred = Fred()
        except:
            pass
    
    def get_gdp_data(self):
        """Get GDP data and growth rates"""
        try:
            if self.fred:
                # Get quarterly GDP data
                gdp = self.fred.get_series('GDP', limit=20)  # Real GDP
                gdp_per_capita = self.fred.get_series('A939RX0Q048SBEA', limit=20)  # Real GDP per capita
                
                # Calculate growth rates
                gdp_growth = gdp.pct_change(periods=4) * 100  # Year-over-year growth
                gdp_per_capita_growth = gdp_per_capita.pct_change(periods=4) * 100
                
                return {
                    'gdp_current': gdp.iloc[-1] if not gdp.empty else None,
                    'gdp_growth': gdp_growth.iloc[-1] if not gdp_growth.empty else None,
                    'gdp_per_capita': gdp_per_capita.iloc[-1] if not gdp_per_capita.empty else None,
                    'gdp_per_capita_growth': gdp_per_capita_growth.iloc[-1] if not gdp_per_capita_growth.empty else None,
                    'gdp_trend': 'Positive' if gdp_growth.iloc[-1] > 0 else 'Negative' if gdp_growth.iloc[-1] < 0 else 'Neutral'
                }
        except Exception as e:
            pass
        
        # Fallback: Return typical economic indicators for analysis
        return {
            'gdp_current': None,
            'gdp_growth': None,
            'gdp_per_capita': None,
            'gdp_per_capita_growth': None,
            'gdp_trend': 'Data Unavailable'
        }
    
    def get_inflation_data(self):
        """Get inflation data (CPI)"""
        try:
            if self.fred:
                cpi = self.fred.get_series('CPIAUCSL', limit=24)  # Consumer Price Index
                inflation_rate = cpi.pct_change(periods=12) * 100  # Year-over-year inflation
                
                return {
                    'current_cpi': cpi.iloc[-1] if not cpi.empty else None,
                    'inflation_rate': inflation_rate.iloc[-1] if not inflation_rate.empty else None,
                    'inflation_trend': 'Rising' if inflation_rate.iloc[-1] > 2 else 'Moderate' if inflation_rate.iloc[-1] > 0 else 'Deflation'
                }
        except:
            pass
        
        return {
            'current_cpi': None,
            'inflation_rate': None,
            'inflation_trend': 'Data Unavailable'
        }
    
    def get_unemployment_data(self):
        """Get unemployment rate data"""
        try:
            if self.fred:
                unemployment = self.fred.get_series('UNRATE', limit=24)  # Unemployment rate
                
                return {
                    'unemployment_rate': unemployment.iloc[-1] if not unemployment.empty else None,
                    'unemployment_trend': 'Improving' if unemployment.iloc[-1] < unemployment.iloc[-2] else 'Worsening' if unemployment.iloc[-1] > unemployment.iloc[-2] else 'Stable'
                }
        except:
            pass
        
        return {
            'unemployment_rate': None,
            'unemployment_trend': 'Data Unavailable'
        }
    
    def get_interest_rates(self):
        """Get federal funds rate and treasury yields"""
        try:
            if self.fred:
                fed_rate = self.fred.get_series('FEDFUNDS', limit=12)  # Federal funds rate
                treasury_10y = self.fred.get_series('GS10', limit=12)  # 10-year treasury
                
                return {
                    'fed_funds_rate': fed_rate.iloc[-1] if not fed_rate.empty else None,
                    'treasury_10y': treasury_10y.iloc[-1] if not treasury_10y.empty else None,
                    'rate_environment': 'Rising' if fed_rate.iloc[-1] > fed_rate.iloc[-2] else 'Falling' if fed_rate.iloc[-1] < fed_rate.iloc[-2] else 'Stable'
                }
        except:
            pass
        
        return {
            'fed_funds_rate': None,
            'treasury_10y': None,
            'rate_environment': 'Data Unavailable'
        }
    
    def analyze_economic_impact_on_stock(self, stock_info, sector):
        """Analyze how macroeconomic factors might impact a specific stock"""
        
        # Get economic data
        gdp_data = self.get_gdp_data()
        inflation_data = self.get_inflation_data()
        unemployment_data = self.get_unemployment_data()
        interest_data = self.get_interest_rates()
        
        impact_analysis = {
            'overall_economic_sentiment': 'Neutral',
            'gdp_impact': 'Neutral',
            'inflation_impact': 'Neutral',
            'interest_rate_impact': 'Neutral',
            'sector_specific_impact': 'Neutral',
            'recommendations': []
        }
        
        # Analyze GDP impact
        if gdp_data['gdp_growth']:
            if gdp_data['gdp_growth'] > 2:
                impact_analysis['gdp_impact'] = 'Positive'
                impact_analysis['recommendations'].append('Strong GDP growth supports consumer spending and business investment')
            elif gdp_data['gdp_growth'] < 0:
                impact_analysis['gdp_impact'] = 'Negative'
                impact_analysis['recommendations'].append('GDP contraction may reduce corporate earnings')
        
        # Analyze inflation impact
        if inflation_data['inflation_rate']:
            if inflation_data['inflation_rate'] > 4:
                impact_analysis['inflation_impact'] = 'Negative'
                impact_analysis['recommendations'].append('High inflation may pressure profit margins and consumer spending')
            elif 2 <= inflation_data['inflation_rate'] <= 3:
                impact_analysis['inflation_impact'] = 'Positive'
                impact_analysis['recommendations'].append('Moderate inflation indicates healthy economic growth')
        
        # Analyze interest rate impact based on sector
        if interest_data['fed_funds_rate']:
            if sector in ['Financial Services', 'Banking']:
                if interest_data['fed_funds_rate'] > 3:
                    impact_analysis['interest_rate_impact'] = 'Positive'
                    impact_analysis['sector_specific_impact'] = 'Positive'
                    impact_analysis['recommendations'].append('Higher interest rates benefit financial sector margins')
            elif sector in ['Real Estate', 'Utilities', 'REITs']:
                if interest_data['fed_funds_rate'] > 4:
                    impact_analysis['interest_rate_impact'] = 'Negative'
                    impact_analysis['sector_specific_impact'] = 'Negative'
                    impact_analysis['recommendations'].append('High interest rates may pressure rate-sensitive sectors')
            elif sector == 'Technology':
                if interest_data['fed_funds_rate'] > 4:
                    impact_analysis['interest_rate_impact'] = 'Negative'
                    impact_analysis['recommendations'].append('Higher rates may reduce tech valuations and growth investments')
        
        # Sector-specific economic sensitivity analysis
        sector_sensitivities = {
            'Consumer Cyclical': {
                'gdp_sensitivity': 'High',
                'inflation_sensitivity': 'High',
                'interest_sensitivity': 'Medium',
                'unemployment_sensitivity': 'High'
            },
            'Technology': {
                'gdp_sensitivity': 'Medium',
                'inflation_sensitivity': 'Medium',
                'interest_sensitivity': 'High',
                'unemployment_sensitivity': 'Low'
            },
            'Financial Services': {
                'gdp_sensitivity': 'High',
                'inflation_sensitivity': 'Medium',
                'interest_sensitivity': 'High',
                'unemployment_sensitivity': 'High'
            },
            'Healthcare': {
                'gdp_sensitivity': 'Low',
                'inflation_sensitivity': 'Low',
                'interest_sensitivity': 'Low',
                'unemployment_sensitivity': 'Low'
            },
            'Energy': {
                'gdp_sensitivity': 'High',
                'inflation_sensitivity': 'High',
                'interest_sensitivity': 'Medium',
                'unemployment_sensitivity': 'Medium'
            },
            'Utilities': {
                'gdp_sensitivity': 'Low',
                'inflation_sensitivity': 'Medium',
                'interest_sensitivity': 'High',
                'unemployment_sensitivity': 'Low'
            }
        }
        
        sector_info = sector_sensitivities.get(sector, {
            'gdp_sensitivity': 'Medium',
            'inflation_sensitivity': 'Medium',
            'interest_sensitivity': 'Medium',
            'unemployment_sensitivity': 'Medium'
        })
        
        # Calculate overall economic sentiment
        positive_factors = sum(1 for impact in [
            impact_analysis['gdp_impact'],
            impact_analysis['inflation_impact'],
            impact_analysis['interest_rate_impact']
        ] if impact == 'Positive')
        
        negative_factors = sum(1 for impact in [
            impact_analysis['gdp_impact'],
            impact_analysis['inflation_impact'],
            impact_analysis['interest_rate_impact']
        ] if impact == 'Negative')
        
        if positive_factors > negative_factors:
            impact_analysis['overall_economic_sentiment'] = 'Positive'
        elif negative_factors > positive_factors:
            impact_analysis['overall_economic_sentiment'] = 'Negative'
        
        return {
            'economic_data': {
                'gdp': gdp_data,
                'inflation': inflation_data,
                'unemployment': unemployment_data,
                'interest_rates': interest_data
            },
            'impact_analysis': impact_analysis,
            'sector_sensitivity': sector_info
        }
    
    def get_market_indicators(self):
        """Get additional market indicators"""
        try:
            # Get VIX (volatility index) from Yahoo Finance
            vix = yf.Ticker("^VIX")
            vix_data = vix.history(period="5d")
            
            # Get S&P 500 for market context
            sp500 = yf.Ticker("^GSPC")
            sp500_data = sp500.history(period="1mo")
            
            if not vix_data.empty and not sp500_data.empty:
                vix_current = vix_data['Close'].iloc[-1]
                sp500_return = (sp500_data['Close'].iloc[-1] / sp500_data['Close'].iloc[0] - 1) * 100
                
                return {
                    'vix': vix_current,
                    'market_sentiment': 'Fear' if vix_current > 30 else 'Greed' if vix_current < 15 else 'Neutral',
                    'sp500_monthly_return': sp500_return
                }
        except:
            pass
        
        return {
            'vix': None,
            'market_sentiment': 'Data Unavailable',
            'sp500_monthly_return': None
        }