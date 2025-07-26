import pandas as pd
import numpy as np

def get_recommendation(ticker, info, hist_data):
    """
    Generate investment recommendation based on multiple factors
    """
    try:
        recommendation_score = 0
        factors = {}
        
        # Factor 1: Valuation (P/E ratio analysis)
        pe_ratio = info.get('trailingPE', 0)
        if pe_ratio:
            if pe_ratio < 15:
                recommendation_score += 2
                factors['Valuation (P/E)'] = "Undervalued (P/E < 15)"
            elif pe_ratio < 25:
                recommendation_score += 1
                factors['Valuation (P/E)'] = "Fairly valued (P/E 15-25)"
            else:
                recommendation_score -= 1
                factors['Valuation (P/E)'] = "Overvalued (P/E > 25)"
        else:
            factors['Valuation (P/E)'] = "P/E data not available"
        
        # Factor 2: Price momentum (comparing current price to moving averages)
        if not hist_data.empty and len(hist_data) >= 50:
            current_price = hist_data['Close'].iloc[-1]
            ma_20 = hist_data['Close'].rolling(20).mean().iloc[-1]
            ma_50 = hist_data['Close'].rolling(50).mean().iloc[-1]
            
            if current_price > ma_20 > ma_50:
                recommendation_score += 2
                factors['Price Momentum'] = "Strong uptrend (above 20-day and 50-day MA)"
            elif current_price > ma_20:
                recommendation_score += 1
                factors['Price Momentum'] = "Positive momentum (above 20-day MA)"
            elif current_price < ma_50:
                recommendation_score -= 1
                factors['Price Momentum'] = "Weak momentum (below 50-day MA)"
            else:
                factors['Price Momentum'] = "Neutral momentum"
        else:
            factors['Price Momentum'] = "Insufficient data for momentum analysis"
        
        # Factor 3: RSI analysis
        if not hist_data.empty and len(hist_data) >= 14:
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            
            if pd.notna(current_rsi):
                if current_rsi < 30:
                    recommendation_score += 1
                    factors['Technical (RSI)'] = f"Oversold (RSI: {current_rsi:.1f})"
                elif current_rsi > 70:
                    recommendation_score -= 1
                    factors['Technical (RSI)'] = f"Overbought (RSI: {current_rsi:.1f})"
                else:
                    factors['Technical (RSI)'] = f"Neutral (RSI: {current_rsi:.1f})"
            else:
                factors['Technical (RSI)'] = "RSI calculation not available"
        else:
            factors['Technical (RSI)'] = "Insufficient data for RSI"
        
        # Factor 4: Financial health
        debt_to_equity = info.get('debtToEquity', 0)
        if debt_to_equity:
            if debt_to_equity < 0.3:
                recommendation_score += 1
                factors['Financial Health'] = "Strong balance sheet (low debt)"
            elif debt_to_equity > 1.0:
                recommendation_score -= 1
                factors['Financial Health'] = "High debt levels"
            else:
                factors['Financial Health'] = "Moderate debt levels"
        else:
            factors['Financial Health'] = "Debt information not available"
        
        # Factor 5: Dividend yield
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield:
            if dividend_yield > 0.03:  # > 3%
                recommendation_score += 1
                factors['Dividend'] = f"Attractive dividend yield ({dividend_yield*100:.1f}%)"
            else:
                factors['Dividend'] = f"Moderate dividend yield ({dividend_yield*100:.1f}%)"
        else:
            factors['Dividend'] = "No dividend or data not available"
        
        # Factor 6: Revenue and earnings growth
        revenue_growth = info.get('revenueGrowth', 0)
        earnings_growth = info.get('earningsGrowth', 0)
        
        if revenue_growth and revenue_growth > 0.05:  # > 5% growth
            recommendation_score += 1
            factors['Revenue Growth'] = f"Strong revenue growth ({revenue_growth*100:.1f}%)"
        elif revenue_growth and revenue_growth < 0:
            recommendation_score -= 1
            factors['Revenue Growth'] = f"Declining revenue ({revenue_growth*100:.1f}%)"
        else:
            factors['Revenue Growth'] = "Moderate or unknown revenue growth"
        
        # Generate final recommendation
        if recommendation_score >= 4:
            action = "STRONG BUY"
            reason = "Multiple positive indicators suggest strong upside potential"
        elif recommendation_score >= 2:
            action = "BUY"
            reason = "Overall positive outlook with good risk-reward ratio"
        elif recommendation_score >= 0:
            action = "HOLD"
            reason = "Mixed signals suggest maintaining current position"
        elif recommendation_score >= -2:
            action = "WEAK SELL"
            reason = "Some concerning factors but not necessarily time to exit"
        else:
            action = "SELL"
            reason = "Multiple negative indicators suggest significant downside risk"
        
        # Risk assessment
        volatility = hist_data['Close'].pct_change().std() * np.sqrt(252) if not hist_data.empty else 0
        
        if volatility > 0.4:  # > 40% annual volatility
            risk_level = "High"
        elif volatility > 0.25:  # > 25% annual volatility
            risk_level = "Moderate"
        else:
            risk_level = "Low"
        
        risk_assessment = f"Risk Level: {risk_level} (Annual volatility: {volatility*100:.1f}%)"
        
        return {
            'action': action,
            'reason': reason,
            'score': recommendation_score,
            'factors': factors,
            'risk_assessment': risk_assessment
        }
    
    except Exception as e:
        return {
            'action': 'HOLD',
            'reason': f'Unable to generate recommendation due to data limitations: {str(e)}',
            'score': 0,
            'factors': {'Error': 'Insufficient data for analysis'},
            'risk_assessment': 'Risk assessment unavailable'
        }

def get_sector_analysis(info):
    """
    Provide sector-specific analysis and benchmarks
    """
    sector = info.get('sector', 'Unknown')
    industry = info.get('industry', 'Unknown')
    
    sector_insights = {
        'Technology': {
            'key_metrics': ['P/E ratio', 'Revenue growth', 'R&D spending'],
            'typical_pe': 25,
            'growth_expectation': 'High',
            'volatility': 'High'
        },
        'Healthcare': {
            'key_metrics': ['P/E ratio', 'Pipeline strength', 'Regulatory approvals'],
            'typical_pe': 20,
            'growth_expectation': 'Moderate',
            'volatility': 'Moderate'
        },
        'Financial Services': {
            'key_metrics': ['P/B ratio', 'ROE', 'Net interest margin'],
            'typical_pe': 12,
            'growth_expectation': 'Low-Moderate',
            'volatility': 'Moderate'
        }
    }
    
    return sector_insights.get(sector, {
        'key_metrics': ['P/E ratio', 'Revenue growth', 'Debt levels'],
        'typical_pe': 18,
        'growth_expectation': 'Moderate',
        'volatility': 'Moderate'
    })
