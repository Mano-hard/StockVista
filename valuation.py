import pandas as pd
import numpy as np
from datetime import datetime

def calculate_dcf_value(ticker, info):
    """
    Calculate Discounted Cash Flow (DCF) valuation
    """
    try:
        # Get cash flow statement
        cash_flow = ticker.cashflow
        
        if cash_flow.empty:
            return None
        
        # Get the most recent free cash flow
        if 'Free Cash Flow' in cash_flow.index:
            recent_fcf = cash_flow.loc['Free Cash Flow'].iloc[0]
        elif 'Operating Cash Flow' in cash_flow.index:
            # Approximate FCF using operating cash flow
            operating_cf = cash_flow.loc['Operating Cash Flow'].iloc[0]
            # Assume capex is 5% of revenue as approximation
            revenue = info.get('totalRevenue', 0)
            capex = revenue * 0.05 if revenue else 0
            recent_fcf = operating_cf - capex
        else:
            return None
        
        if pd.isna(recent_fcf) or recent_fcf <= 0:
            return None
        
        # DCF assumptions
        growth_rate = 0.05  # 5% perpetual growth rate
        discount_rate = 0.10  # 10% discount rate (WACC approximation)
        terminal_growth = 0.02  # 2% terminal growth rate
        
        # Calculate terminal value
        terminal_fcf = recent_fcf * (1 + growth_rate) ** 5 * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        
        # Calculate present value of projected cash flows (5 years)
        pv_fcf = 0
        for year in range(1, 6):
            projected_fcf = recent_fcf * (1 + growth_rate) ** year
            pv_fcf += projected_fcf / (1 + discount_rate) ** year
        
        # Present value of terminal value
        pv_terminal = terminal_value / (1 + discount_rate) ** 5
        
        # Enterprise value
        enterprise_value = pv_fcf + pv_terminal
        
        # Get shares outstanding
        shares_outstanding = info.get('sharesOutstanding', 0)
        if not shares_outstanding:
            return None
        
        # Calculate per share value
        fair_value_per_share = enterprise_value / shares_outstanding
        
        return fair_value_per_share
    
    except Exception:
        return None

def calculate_pe_valuation(ticker, info):
    """
    Calculate fair value based on P/E ratio comparison
    """
    try:
        # Get current EPS
        eps = info.get('trailingEps', 0)
        if not eps or eps <= 0:
            return None
        
        # Get industry/sector average P/E (approximation)
        current_pe = info.get('trailingPE', 0)
        if not current_pe:
            return None
        
        # Use sector median P/E as benchmark
        # This is a simplified approach - in practice, you'd compare to industry peers
        sector_pe_estimates = {
            'Technology': 25,
            'Healthcare': 20,
            'Financial Services': 12,
            'Consumer Cyclical': 18,
            'Consumer Defensive': 22,
            'Energy': 15,
            'Utilities': 16,
            'Real Estate': 20,
            'Materials': 16,
            'Industrials': 18,
            'Communication Services': 20
        }
        
        sector = info.get('sector', 'Technology')
        benchmark_pe = sector_pe_estimates.get(sector, 20)  # Default to 20 if sector not found
        
        # Calculate fair value using benchmark P/E
        fair_value = eps * benchmark_pe
        
        return fair_value
    
    except Exception:
        return None

def calculate_graham_number(ticker, info):
    """
    Calculate Benjamin Graham's fair value formula
    """
    try:
        eps = info.get('trailingEps', 0)
        book_value_per_share = info.get('bookValue', 0)
        
        if not eps or not book_value_per_share or eps <= 0 or book_value_per_share <= 0:
            return None
        
        # Graham's formula: √(22.5 × EPS × Book Value per Share)
        graham_number = (22.5 * eps * book_value_per_share) ** 0.5
        
        return graham_number
    
    except Exception:
        return None

def calculate_peg_ratio(ticker, info):
    """
    Calculate PEG ratio (P/E to Growth ratio)
    """
    try:
        pe_ratio = info.get('trailingPE', 0)
        growth_rate = info.get('earningsGrowth', 0)
        
        if not pe_ratio or not growth_rate or growth_rate <= 0:
            return None
        
        # Convert growth rate to percentage
        growth_rate_pct = growth_rate * 100
        
        peg_ratio = pe_ratio / growth_rate_pct
        
        return peg_ratio
    
    except Exception:
        return None
