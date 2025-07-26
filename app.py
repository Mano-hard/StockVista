import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
from valuation import calculate_dcf_value, calculate_pe_valuation
from recommendations import get_recommendation
from economic_indicators import EconomicAnalyzer
from company_search import CompanySearcher, ProfitCompoundingAnalyzer
# from database import db_manager  # Removed as requested

# Configure page
st.set_page_config(
    page_title="Equity Research Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Main title and search interface
st.title("📈 Equity Research Platform")
st.markdown("---")

# Initialize company searcher
if 'company_searcher' not in st.session_state:
    st.session_state.company_searcher = CompanySearcher()

# Professional Services Section
with st.sidebar:
    st.markdown("## 🎯 Professional Research Services")
    
    st.markdown("### 📊 Get Expert Analysis")
    st.markdown("**Manohar Mazumdar**")
    st.markdown("*NISM Certified Research Analyst*")
    
    st.markdown("---")
    st.markdown("**Professional Services:**")
    st.markdown("• Comprehensive equity research")
    st.markdown("• Portfolio analysis & recommendations")
    st.markdown("• Market trend analysis")
    st.markdown("• Investment strategy consultation")
    
    st.markdown("---")
    st.markdown("**Investment Advisory:**")
    st.markdown("**₹1,00,000 per year**")
    
    st.markdown("---")
    st.markdown("**Contact for Full Support:**")
    st.markdown("📧 **Email:** manoharmazumdar@gmail.com")
    st.markdown("📱 **WhatsApp:** +91 9474272743")
    
    st.markdown("---")
    
    # Contact button
    if st.button("📞 Contact for Professional Advisory", use_container_width=True, type="primary"):
        st.success("Contact Manohar Mazumdar at the details above for personalized investment advisory services!")
    
    st.markdown("---")
    st.markdown("*This platform provides educational analysis. For personalized investment advice, contact our certified research analyst.*")

# Center the search box with prominent styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### Which equity are you going to research?")
    st.markdown("*Enter company name or stock symbol (US & Indian stocks supported)*")
    
    user_input = st.text_input(
        "Stock Symbol or Company Name",
        placeholder="e.g., Apple, TCS, AAPL, RELIANCE.NS, Microsoft",
        key="stock_input",
        label_visibility="collapsed"
    )
    
    # Show suggestions as user types
    if user_input and len(user_input) >= 2:
        suggestions = st.session_state.company_searcher.get_suggestions(user_input)
        if suggestions:
            st.markdown("**Suggestions:**")
            for suggestion in suggestions:
                st.write(f"• {suggestion['name']} ({suggestion['symbol']}) - {suggestion['exchange']}")
    
    search_button = st.button("🔍 Research Stock", use_container_width=True, type="primary")

if search_button and user_input:
    try:
        # Search for the company and get the appropriate ticker symbol
        stock_symbol = st.session_state.company_searcher.search_company(user_input)
        
        # Note: Database functionality removed as requested
        
        # Initialize the ticker
        ticker = yf.Ticker(stock_symbol)
        
        # Get stock info
        info = ticker.info
        if not info or 'symbol' not in info:
            st.error(f"❌ Stock symbol '{stock_symbol.upper()}' not found. Please check the symbol and try again.")
            st.stop()
        
        # Display company information
        st.markdown("---")
        company_name = info.get('longName', stock_symbol.upper())
        
        # Company header
        st.markdown(f"## {company_name} ({info.get('symbol', stock_symbol.upper())})")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Overview", "📈 Price Analysis", "💰 Valuation", "🎯 Recommendation", "🌍 Economic Impact", "📈 Profit Compounding", "📋 Financial Data"])
        
        with tab1:
            # Company overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
                st.metric("Market Cap", f"${info.get('marketCap', 0):,.0f}" if info.get('marketCap') else "N/A")
            
            with col2:
                previous_close = info.get('previousClose', 0)
                current_price = info.get('currentPrice', 0)
                change = current_price - previous_close if current_price and previous_close else 0
                change_percent = (change / previous_close * 100) if previous_close else 0
                st.metric("Daily Change", f"${change:.2f}", f"{change_percent:.2f}%")
                st.metric("Volume", f"{info.get('volume', 0):,}")
            
            with col3:
                st.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
                st.metric("Dividend Yield", f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A")
            
            with col4:
                st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
                st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
            
            # Company description
            if info.get('longBusinessSummary'):
                st.markdown("### Company Overview")
                st.write(info['longBusinessSummary'])
        
        with tab2:
            # Price analysis with charts
            st.markdown("### Historical Price Analysis")
            
            # Time period selection
            period_col1, period_col2 = st.columns([1, 3])
            with period_col1:
                period = st.selectbox(
                    "Select Time Period:",
                    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                    index=3
                )
            
            # Get historical data
            hist_data = ticker.history(period=period)
            
            if not hist_data.empty:
                # Create price chart
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.03,
                    subplot_titles=('Price Movement', 'Volume'),
                    row_width=[0.2, 0.7]
                )
                
                # Add candlestick chart
                fig.add_trace(
                    go.Candlestick(
                        x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close'],
                        name="Price"
                    ),
                    row=1, col=1
                )
                
                # Add volume bars
                fig.add_trace(
                    go.Bar(
                        x=hist_data.index,
                        y=hist_data['Volume'],
                        name="Volume",
                        marker_color='rgba(158,202,225,0.8)'
                    ),
                    row=2, col=1
                )
                
                fig.update_layout(
                    title=f"{stock_symbol.upper()} Price and Volume",
                    yaxis_title="Price ($)",
                    yaxis2_title="Volume",
                    xaxis_rangeslider_visible=False,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                st.markdown("### Technical Indicators")
                
                # Calculate moving averages
                hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
                hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
                
                # RSI calculation
                delta = hist_data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                hist_data['RSI'] = 100 - (100 / (1 + rs))
                
                # Display latest technical indicators
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("20-Day MA", f"${hist_data['MA20'].iloc[-1]:.2f}" if not pd.isna(hist_data['MA20'].iloc[-1]) else "N/A")
                with col2:
                    st.metric("50-Day MA", f"${hist_data['MA50'].iloc[-1]:.2f}" if not pd.isna(hist_data['MA50'].iloc[-1]) else "N/A")
                with col3:
                    st.metric("RSI (14)", f"{hist_data['RSI'].iloc[-1]:.2f}" if not pd.isna(hist_data['RSI'].iloc[-1]) else "N/A")
                with col4:
                    volatility = hist_data['Close'].pct_change().std() * np.sqrt(252) * 100
                    st.metric("Volatility (Annual)", f"{volatility:.2f}%")
        
        with tab3:
            # Valuation analysis
            st.markdown("### Fair Value Analysis")
            
            # Get financial data for valuation
            try:
                financials = ticker.financials
                balance_sheet = ticker.balance_sheet
                cash_flow = ticker.cashflow
                
                val_col1, val_col2 = st.columns(2)
                
                with val_col1:
                    st.markdown("#### DCF Valuation")
                    dcf_value = calculate_dcf_value(ticker, info)
                    if dcf_value:
                        st.metric("DCF Fair Value", f"${dcf_value:.2f}")
                        current_price = info.get('currentPrice', 0)
                        if current_price:
                            upside = ((dcf_value - current_price) / current_price) * 100
                            st.metric("Upside/Downside", f"{upside:.1f}%")
                    else:
                        st.write("DCF calculation not available due to insufficient data")
                
                with val_col2:
                    st.markdown("#### P/E Comparison")
                    pe_value = calculate_pe_valuation(ticker, info)
                    if pe_value:
                        st.metric("P/E Based Fair Value", f"${pe_value:.2f}")
                        current_price = info.get('currentPrice', 0)
                        if current_price:
                            upside = ((pe_value - current_price) / current_price) * 100
                            st.metric("Upside/Downside", f"{upside:.1f}%")
                    else:
                        st.write("P/E valuation not available")
                
                # Valuation multiples table
                st.markdown("#### Key Valuation Metrics")
                metrics_data = {
                    'Metric': ['P/E Ratio', 'P/B Ratio', 'P/S Ratio', 'EV/EBITDA', 'Debt/Equity'],
                    'Current Value': [
                        f"{info.get('trailingPE', 'N/A')}",
                        f"{info.get('priceToBook', 'N/A')}",
                        f"{info.get('priceToSalesTrailing12Months', 'N/A')}",
                        f"{info.get('enterpriseToEbitda', 'N/A')}",
                        f"{info.get('debtToEquity', 'N/A')}"
                    ]
                }
                st.table(pd.DataFrame(metrics_data))
                
            except Exception as e:
                st.error(f"Error loading financial data for valuation: {str(e)}")
        
        with tab4:
            # Investment recommendation
            st.markdown("### Investment Recommendation")
            
            recommendation = get_recommendation(ticker, info, hist_data)
            
            # Display recommendation with color coding
            if recommendation['action'] == 'BUY':
                st.success(f"🟢 **{recommendation['action']}** - {recommendation['reason']}")
            elif recommendation['action'] == 'SELL':
                st.error(f"🔴 **{recommendation['action']}** - {recommendation['reason']}")
            else:
                st.warning(f"🟡 **{recommendation['action']}** - {recommendation['reason']}")
            
            # Recommendation details
            st.markdown("#### Analysis Summary")
            for factor, score in recommendation['factors'].items():
                st.write(f"• **{factor}**: {score}")
            
            # Risk assessment
            st.markdown("#### Risk Assessment")
            st.write(recommendation['risk_assessment'])
        
        with tab5:
            # Economic impact analysis
            st.markdown("### Macroeconomic Impact Analysis")
            
            # Initialize economic analyzer
            economic_analyzer = EconomicAnalyzer()
            sector = info.get('sector', 'Unknown')
            
            # Get economic analysis
            with st.spinner("Analyzing macroeconomic factors..."):
                economic_analysis = economic_analyzer.analyze_economic_impact_on_stock(info, sector)
                market_indicators = economic_analyzer.get_market_indicators()
            
            # Display overall economic sentiment
            sentiment = economic_analysis['impact_analysis']['overall_economic_sentiment']
            if sentiment == 'Positive':
                st.success(f"🟢 **Economic Environment: {sentiment}** - Favorable macroeconomic conditions")
            elif sentiment == 'Negative':
                st.error(f"🔴 **Economic Environment: {sentiment}** - Challenging macroeconomic conditions")
            else:
                st.warning(f"🟡 **Economic Environment: {sentiment}** - Mixed macroeconomic signals")
            
            # Economic indicators dashboard
            st.markdown("#### Key Economic Indicators")
            
            econ_col1, econ_col2, econ_col3, econ_col4 = st.columns(4)
            
            with econ_col1:
                gdp_data = economic_analysis['economic_data']['gdp']
                if gdp_data['gdp_growth'] is not None:
                    st.metric("GDP Growth (YoY)", f"{gdp_data['gdp_growth']:.1f}%")
                else:
                    st.metric("GDP Growth (YoY)", "N/A")
                
                if gdp_data['gdp_per_capita_growth'] is not None:
                    st.metric("GDP Per Capita Growth", f"{gdp_data['gdp_per_capita_growth']:.1f}%")
                else:
                    st.metric("GDP Per Capita Growth", "N/A")
            
            with econ_col2:
                inflation_data = economic_analysis['economic_data']['inflation']
                if inflation_data['inflation_rate'] is not None:
                    st.metric("Inflation Rate (CPI)", f"{inflation_data['inflation_rate']:.1f}%")
                else:
                    st.metric("Inflation Rate (CPI)", "N/A")
                
                unemployment_data = economic_analysis['economic_data']['unemployment']
                if unemployment_data['unemployment_rate'] is not None:
                    st.metric("Unemployment Rate", f"{unemployment_data['unemployment_rate']:.1f}%")
                else:
                    st.metric("Unemployment Rate", "N/A")
            
            with econ_col3:
                interest_data = economic_analysis['economic_data']['interest_rates']
                if interest_data['fed_funds_rate'] is not None:
                    st.metric("Federal Funds Rate", f"{interest_data['fed_funds_rate']:.2f}%")
                else:
                    st.metric("Federal Funds Rate", "N/A")
                
                if interest_data['treasury_10y'] is not None:
                    st.metric("10-Year Treasury", f"{interest_data['treasury_10y']:.2f}%")
                else:
                    st.metric("10-Year Treasury", "N/A")
            
            with econ_col4:
                if market_indicators['vix'] is not None:
                    st.metric("VIX (Fear Index)", f"{market_indicators['vix']:.1f}")
                    st.metric("Market Sentiment", market_indicators['market_sentiment'])
                else:
                    st.metric("VIX (Fear Index)", "N/A")
                    st.metric("Market Sentiment", "N/A")
            
            # Sector sensitivity analysis
            st.markdown("#### Sector Economic Sensitivity")
            st.markdown(f"**{sector} Sector Characteristics:**")
            
            sensitivity = economic_analysis['sector_sensitivity']
            sens_col1, sens_col2 = st.columns(2)
            
            with sens_col1:
                st.write(f"• **GDP Sensitivity**: {sensitivity.get('gdp_sensitivity', 'Medium')}")
                st.write(f"• **Inflation Sensitivity**: {sensitivity.get('inflation_sensitivity', 'Medium')}")
            
            with sens_col2:
                st.write(f"• **Interest Rate Sensitivity**: {sensitivity.get('interest_sensitivity', 'Medium')}")
                st.write(f"• **Unemployment Sensitivity**: {sensitivity.get('unemployment_sensitivity', 'Medium')}")
            
            # Economic impact summary
            st.markdown("#### Economic Impact Assessment")
            
            impact_summary = economic_analysis['impact_analysis']
            
            # Create impact visualization
            impact_factors = ['GDP Impact', 'Inflation Impact', 'Interest Rate Impact', 'Sector Impact']
            impact_values = [
                1 if impact_summary['gdp_impact'] == 'Positive' else -1 if impact_summary['gdp_impact'] == 'Negative' else 0,
                1 if impact_summary['inflation_impact'] == 'Positive' else -1 if impact_summary['inflation_impact'] == 'Negative' else 0,
                1 if impact_summary['interest_rate_impact'] == 'Positive' else -1 if impact_summary['interest_rate_impact'] == 'Negative' else 0,
                1 if impact_summary['sector_specific_impact'] == 'Positive' else -1 if impact_summary['sector_specific_impact'] == 'Negative' else 0
            ]
            
            # Create bar chart for economic impact
            fig_econ = go.Figure(data=[
                go.Bar(
                    x=impact_factors,
                    y=impact_values,
                    marker_color=['green' if val > 0 else 'red' if val < 0 else 'gray' for val in impact_values],
                    text=[f"{impact_summary['gdp_impact']}", f"{impact_summary['inflation_impact']}", 
                          f"{impact_summary['interest_rate_impact']}", f"{impact_summary['sector_specific_impact']}"],
                    textposition='auto'
                )
            ])
            
            fig_econ.update_layout(
                title="Economic Factors Impact on Stock",
                yaxis_title="Impact Score",
                yaxis=dict(range=[-1.5, 1.5], tickvals=[-1, 0, 1], ticktext=['Negative', 'Neutral', 'Positive']),
                height=400
            )
            
            st.plotly_chart(fig_econ, use_container_width=True)
            
            # Economic recommendations
            st.markdown("#### Economic Environment Insights")
            recommendations = impact_summary.get('recommendations', [])
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            else:
                st.write("Economic data is currently limited. Consider monitoring key indicators:")
                st.write("• GDP growth trends and their impact on corporate earnings")
                st.write("• Inflation effects on input costs and consumer purchasing power")
                st.write("• Interest rate changes affecting borrowing costs and valuations")
                st.write("• Unemployment levels impacting consumer demand")
            
            # Economic data summary for download
            st.markdown("---")
            st.markdown("#### Economic Data Summary")
            
            econ_summary_data = {
                'Indicator': ['GDP Growth Rate', 'GDP Per Capita Growth', 'Inflation Rate', 'Unemployment Rate', 
                             'Federal Funds Rate', '10-Year Treasury', 'VIX', 'Market Sentiment'],
                'Current Value': [
                    f"{gdp_data['gdp_growth']:.1f}%" if gdp_data['gdp_growth'] is not None else "N/A",
                    f"{gdp_data['gdp_per_capita_growth']:.1f}%" if gdp_data['gdp_per_capita_growth'] is not None else "N/A",
                    f"{inflation_data['inflation_rate']:.1f}%" if inflation_data['inflation_rate'] is not None else "N/A",
                    f"{unemployment_data['unemployment_rate']:.1f}%" if unemployment_data['unemployment_rate'] is not None else "N/A",
                    f"{interest_data['fed_funds_rate']:.2f}%" if interest_data['fed_funds_rate'] is not None else "N/A",
                    f"{interest_data['treasury_10y']:.2f}%" if interest_data['treasury_10y'] is not None else "N/A",
                    f"{market_indicators['vix']:.1f}" if market_indicators['vix'] is not None else "N/A",
                    market_indicators['market_sentiment']
                ],
                'Impact on Stock': [
                    impact_summary['gdp_impact'],
                    impact_summary['gdp_impact'],  # GDP per capita follows GDP impact
                    impact_summary['inflation_impact'],
                    'Sector Dependent',
                    impact_summary['interest_rate_impact'],
                    impact_summary['interest_rate_impact'],
                    'Market Volatility Indicator',
                    'Overall Market Mood'
                ]
            }
            
            econ_df = pd.DataFrame(econ_summary_data)
            st.dataframe(econ_df, use_container_width=True)
            
            # Download button for economic analysis
            csv_econ = econ_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Economic Analysis CSV",
                data=csv_econ,
                file_name=f"{stock_symbol}_economic_analysis.csv",
                mime="text/csv"
            )

        with tab6:
            # Profit Compounding Analysis
            st.markdown("### Profit Compounding Analysis")
            st.markdown("*Analyzing whether the company effectively compounds its profits over time*")
            
            # Initialize profit compounding analyzer
            compounding_analyzer = ProfitCompoundingAnalyzer()
            
            with st.spinner("Analyzing profit compounding patterns..."):
                compounding_analysis = compounding_analyzer.analyze_profit_compounding(ticker, info)
            
            # Display overall compounding status
            if compounding_analysis['is_compounding'] is True:
                st.success("🟢 **Strong Profit Compounding** - Company effectively reinvests profits for growth")
            elif compounding_analysis['is_compounding'] is False:
                if compounding_analysis['compounding_score'] >= 3:
                    st.warning("🟡 **Moderate Compounding** - Some positive indicators but room for improvement")
                else:
                    st.error("🔴 **Weak Compounding** - Limited evidence of effective profit reinvestment")
            else:
                st.info("ℹ️ **Insufficient Data** - Unable to determine compounding quality")
            
            # Compounding Score
            st.markdown("#### Compounding Score")
            score = compounding_analysis['compounding_score']
            max_score = 10
            
            # Create a progress bar for the score
            progress_col1, progress_col2 = st.columns([3, 1])
            with progress_col1:
                st.progress(min(score / max_score, 1.0))
            with progress_col2:
                st.metric("Score", f"{score}/{max_score}")
            
            # Key Metrics
            st.markdown("#### Key Growth Metrics")
            
            comp_col1, comp_col2, comp_col3, comp_col4 = st.columns(4)
            
            with comp_col1:
                if compounding_analysis['revenue_growth'] is not None:
                    st.metric("Avg Revenue Growth", f"{compounding_analysis['revenue_growth']:.1f}%")
                else:
                    st.metric("Avg Revenue Growth", "N/A")
            
            with comp_col2:
                if compounding_analysis['profit_growth'] is not None:
                    st.metric("Avg Profit Growth", f"{compounding_analysis['profit_growth']:.1f}%")
                else:
                    st.metric("Avg Profit Growth", "N/A")
            
            with comp_col3:
                if compounding_analysis['roe_trend'] is not None:
                    st.metric("Average ROE", f"{compounding_analysis['roe_trend']:.1f}%")
                else:
                    st.metric("Average ROE", "N/A")
            
            with comp_col4:
                if compounding_analysis['retained_earnings_growth'] is not None:
                    st.metric("Retained Earnings Growth", f"{compounding_analysis['retained_earnings_growth']:.1f}%")
                else:
                    st.metric("Retained Earnings Growth", "N/A")
            
            # Positive Factors
            if compounding_analysis['compounding_factors']:
                st.markdown("#### ✅ Positive Compounding Factors")
                for factor in compounding_analysis['compounding_factors']:
                    st.write(f"• {factor}")
            
            # Warnings/Concerns
            if compounding_analysis['warnings']:
                st.markdown("#### ⚠️ Areas of Concern")
                for warning in compounding_analysis['warnings']:
                    st.write(f"• {warning}")
            
            # Compounding Quality Visualization
            if compounding_analysis['revenue_growth'] is not None and compounding_analysis['profit_growth'] is not None:
                st.markdown("#### Growth Trends Visualization")
                
                # Create a scatter plot showing revenue vs profit growth
                fig_compound = go.Figure()
                
                fig_compound.add_trace(go.Scatter(
                    x=[compounding_analysis['revenue_growth']],
                    y=[compounding_analysis['profit_growth']],
                    mode='markers',
                    marker=dict(
                        size=20,
                        color='green' if compounding_analysis['is_compounding'] else 'orange' if compounding_analysis['compounding_score'] >= 3 else 'red',
                        symbol='diamond'
                    ),
                    name=info.get('longName', stock_symbol),
                    text=[f"{info.get('longName', stock_symbol)}<br>Score: {score}"],
                    textposition="top center"
                ))
                
                # Add ideal quadrant references
                fig_compound.add_hline(y=10, line_dash="dash", line_color="gray", annotation_text="10% Profit Growth")
                fig_compound.add_vline(x=5, line_dash="dash", line_color="gray", annotation_text="5% Revenue Growth")
                
                fig_compound.update_layout(
                    title="Revenue vs Profit Growth Analysis",
                    xaxis_title="Average Revenue Growth (%)",
                    yaxis_title="Average Profit Growth (%)",
                    height=400,
                    showlegend=False
                )
                
                # Add quadrant labels
                fig_compound.add_annotation(x=15, y=25, text="Ideal Zone<br>(High Growth)", showarrow=False, font=dict(color="green", size=10))
                fig_compound.add_annotation(x=-5, y=-10, text="Decline Zone<br>(Negative Growth)", showarrow=False, font=dict(color="red", size=10))
                
                st.plotly_chart(fig_compound, use_container_width=True)
            
            # Management Efficiency
            st.markdown("#### Management Efficiency Indicators")
            
            efficiency = compounding_analysis['efficiency_metrics']
            debt_mgmt = compounding_analysis['debt_management']
            
            eff_col1, eff_col2 = st.columns(2)
            
            with eff_col1:
                if 'profit_margin' in efficiency:
                    margin_status = "Excellent" if efficiency['profit_margin'] > 15 else "Good" if efficiency['profit_margin'] > 10 else "Average"
                    st.metric("Profit Margin", f"{efficiency['profit_margin']:.1f}%", delta=margin_status)
                else:
                    st.metric("Profit Margin", "N/A")
            
            with eff_col2:
                if debt_mgmt is not None:
                    debt_status = "Conservative" if debt_mgmt < 0.3 else "Moderate" if debt_mgmt < 1.0 else "High"
                    st.metric("Debt-to-Equity Ratio", f"{debt_mgmt:.2f}", delta=debt_status)
                else:
                    st.metric("Debt-to-Equity Ratio", "N/A")
            
            # Recommendation
            st.markdown("#### Compounding Assessment")
            recommendation = compounding_analyzer.get_compounding_recommendation(compounding_analysis)
            
            if compounding_analysis['is_compounding'] is True:
                st.success(f"📈 **{recommendation}**")
            elif compounding_analysis['is_compounding'] is False:
                if compounding_analysis['compounding_score'] >= 3:
                    st.warning(f"📊 **{recommendation}**")
                else:
                    st.error(f"📉 **{recommendation}**")
            else:
                st.info(f"ℹ️ **{recommendation}**")
            
            # What to look for in compounding
            st.markdown("---")
            st.markdown("#### Understanding Profit Compounding")
            
            with st.expander("What makes a good compounding company?"):
                st.write("""
                **Key Characteristics of Compounding Companies:**
                
                1. **Consistent Revenue Growth**: Companies that consistently grow their top-line revenue
                2. **Expanding Profit Margins**: Ability to increase profitability over time
                3. **High Return on Equity (ROE)**: Efficient use of shareholder equity (>15% is excellent)
                4. **Growing Retained Earnings**: Company reinvests profits rather than just paying dividends
                5. **Conservative Debt Management**: Maintains reasonable debt levels for sustainable growth
                6. **Operational Efficiency**: Improving profit margins and operational metrics
                
                **Why Compounding Matters:**
                - Compounding companies can create exponential wealth over long periods
                - They reinvest profits effectively to generate higher future returns
                - Less dependence on market timing and economic cycles
                - Warren Buffett's favorite type of investment
                """)
            
            # Download compounding analysis
            st.markdown("---")
            compounding_summary = {
                'Metric': ['Compounding Score', 'Revenue Growth', 'Profit Growth', 'Average ROE', 
                          'Retained Earnings Growth', 'Profit Margin', 'Debt-to-Equity', 'Overall Assessment'],
                'Value': [
                    f"{score}/{max_score}",
                    f"{compounding_analysis['revenue_growth']:.1f}%" if compounding_analysis['revenue_growth'] is not None else "N/A",
                    f"{compounding_analysis['profit_growth']:.1f}%" if compounding_analysis['profit_growth'] is not None else "N/A",
                    f"{compounding_analysis['roe_trend']:.1f}%" if compounding_analysis['roe_trend'] is not None else "N/A",
                    f"{compounding_analysis['retained_earnings_growth']:.1f}%" if compounding_analysis['retained_earnings_growth'] is not None else "N/A",
                    f"{efficiency['profit_margin']:.1f}%" if 'profit_margin' in efficiency else "N/A",
                    f"{debt_mgmt:.2f}" if debt_mgmt is not None else "N/A",
                    "Strong" if compounding_analysis['is_compounding'] is True else "Moderate" if compounding_analysis['compounding_score'] >= 3 else "Weak"
                ]
            }
            
            compounding_df = pd.DataFrame(compounding_summary)
            st.dataframe(compounding_df, use_container_width=True)
            
            csv_compounding = compounding_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Compounding Analysis CSV",
                data=csv_compounding,
                file_name=f"{stock_symbol}_compounding_analysis.csv",
                mime="text/csv"
            )

        with tab7:
            # Financial data tables
            st.markdown("### Financial Statements")
            
            try:
                # Get financial statements
                financials = ticker.financials
                balance_sheet = ticker.balance_sheet
                cash_flow = ticker.cashflow
                
                # Create sub-tabs for different statements
                fin_tab1, fin_tab2, fin_tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
                
                with fin_tab1:
                    if not financials.empty:
                        st.markdown("#### Income Statement (Annual)")
                        # Transpose for better readability
                        income_df = financials.T
                        income_df.index = income_df.index.to_series().dt.strftime('%Y')
                        st.dataframe(income_df, use_container_width=True)
                        
                        # Download button for income statement
                        csv_income = income_df.to_csv()
                        st.download_button(
                            label="📥 Download Income Statement CSV",
                            data=csv_income,
                            file_name=f"{stock_symbol}_income_statement.csv",
                            mime="text/csv"
                        )
                    else:
                        st.write("Income statement data not available")
                
                with fin_tab2:
                    if not balance_sheet.empty:
                        st.markdown("#### Balance Sheet (Annual)")
                        balance_df = balance_sheet.T
                        balance_df.index = balance_df.index.to_series().dt.strftime('%Y')
                        st.dataframe(balance_df, use_container_width=True)
                        
                        # Download button for balance sheet
                        csv_balance = balance_df.to_csv()
                        st.download_button(
                            label="📥 Download Balance Sheet CSV",
                            data=csv_balance,
                            file_name=f"{stock_symbol}_balance_sheet.csv",
                            mime="text/csv"
                        )
                    else:
                        st.write("Balance sheet data not available")
                
                with fin_tab3:
                    if not cash_flow.empty:
                        st.markdown("#### Cash Flow Statement (Annual)")
                        cashflow_df = cash_flow.T
                        cashflow_df.index = cashflow_df.index.to_series().dt.strftime('%Y')
                        st.dataframe(cashflow_df, use_container_width=True)
                        
                        # Download button for cash flow
                        csv_cashflow = cashflow_df.to_csv()
                        st.download_button(
                            label="📥 Download Cash Flow CSV",
                            data=csv_cashflow,
                            file_name=f"{stock_symbol}_cash_flow.csv",
                            mime="text/csv"
                        )
                    else:
                        st.write("Cash flow data not available")
                
                # Historical price data download
                st.markdown("---")
                st.markdown("#### Historical Price Data")
                if not hist_data.empty:
                    st.dataframe(hist_data.tail(10), use_container_width=True)
                    
                    # Download button for historical data
                    csv_hist = hist_data.to_csv()
                    st.download_button(
                        label="📥 Download Historical Price Data CSV",
                        data=csv_hist,
                        file_name=f"{stock_symbol}_historical_data.csv",
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"Error loading financial statements: {str(e)}")
        
        # Analysis completed
        st.success("✅ Analysis completed successfully!")
    
    except Exception as e:
        st.error(f"❌ Error retrieving data for {stock_symbol.upper()}: {str(e)}")
        st.write("Please check the stock symbol and try again.")

elif search_button and not user_input:
    st.warning("⚠️ Please enter a company name or stock symbol to begin your research.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        📊 Equity Research Platform | Data provided by Yahoo Finance<br>
        <strong>Professional Advisory by Manohar Mazumdar, NISM Certified Research Analyst</strong><br>
        📧 manoharmazumdar@gmail.com | 📱 +91 9474272743<br>
        <em>For personalized investment advisory services - ₹1,00,000 per year</em>
    </div>
    """,
    unsafe_allow_html=True
)
