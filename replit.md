# Equity Research Platform

## Overview

This is a Streamlit-based equity research platform that provides comprehensive stock analysis capabilities. The application leverages financial APIs to retrieve real-time stock data and performs various valuation methods including DCF (Discounted Cash Flow) and P/E ratio analysis. It also generates investment recommendations based on multiple technical and fundamental factors.

## User Preferences

- Preferred communication style: Simple, everyday language
- Interface: Dark theme for professional equity research environment
- Analysis depth: Comprehensive analysis including macroeconomic factors
- Professional Services: Manohar Mazumdar (NISM Certified Research Analyst)
- Contact: manoharmazumdar@gmail.com, +91 9474272743
- Advisory Fee: ₹1,00,000 per year
- Database: Removed as per user request

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **Layout**: Wide layout with collapsible sidebar
- **UI Components**: Centered search interface with three-column layout for optimal user experience
- **Visualization**: Plotly for interactive charts and graphs (both graph_objects and express modules)

### Backend Architecture
- **Language**: Python
- **Architecture Pattern**: Modular design with separated concerns
- **Core Modules**:
  - `app.py`: Main application entry point and UI logic
  - `valuation.py`: Financial valuation calculations (DCF, P/E analysis)
  - `recommendations.py`: Investment recommendation engine

### Data Processing
- **Data Source**: Yahoo Finance API via yfinance library
- **Data Handling**: Pandas for data manipulation and NumPy for numerical computations
- **Real-time Data**: Live stock quotes, historical data, and company fundamentals

## Key Components

### 1. Stock Data Retrieval
- Uses yfinance library to fetch real-time stock information
- Retrieves company info, historical prices, and financial statements
- Implements error handling for invalid stock symbols

### 2. Valuation Engine (`valuation.py`)
- **DCF Calculation**: Implements discounted cash flow model with configurable assumptions
  - 5% perpetual growth rate
  - 10% discount rate (WACC approximation)
  - 2% terminal growth rate
  - 5-year projection period
- **P/E Valuation**: Comparative valuation using price-to-earnings ratios

### 3. Recommendation System (`recommendations.py`)
- **Multi-factor Analysis**: Combines multiple investment factors:
  - Valuation metrics (P/E ratio thresholds)
  - Price momentum analysis (20-day and 50-day moving averages)
  - RSI technical analysis (partially implemented)
- **Scoring System**: Numerical recommendation score with qualitative factors

### 4. Macroeconomic Analysis (`economic_indicators.py`)
- **Economic Data Integration**: Federal Reserve Economic Data (FRED) API integration
- **GDP Analysis**: GDP growth rates and per capita analysis with stock impact assessment
- **Inflation Monitoring**: Consumer Price Index tracking and inflation impact analysis
- **Interest Rate Analysis**: Federal funds rate and treasury yield monitoring
- **Sector Sensitivity**: Customized economic impact analysis by sector
- **Market Indicators**: VIX volatility index and market sentiment analysis

### 5. Company Search System (`company_search.py`)
- **Multi-Market Support**: US (NASDAQ/NYSE) and Indian (NSE/BSE) stock exchanges
- **Intelligent Mapping**: Company name to stock symbol conversion
- **Search Suggestions**: Real-time suggestions with exchange information
- **Partial Matching**: Flexible search with partial name matching capabilities

### 6. Profit Compounding Analysis (`company_search.py`)
- **Growth Analysis**: Multi-year revenue and profit growth assessment
- **ROE Tracking**: Return on equity trends and efficiency analysis
- **Reinvestment Quality**: Retained earnings growth and debt management evaluation
- **Scoring System**: Comprehensive compounding quality scoring (0-10 scale)
- **Visual Analytics**: Growth trend visualization with quadrant analysis

### 7. Database Management (`database.py`)
- **PostgreSQL Integration**: Full database connectivity with SQLAlchemy ORM
- **Data Models**: Comprehensive schema for analyses, watchlists, and search history
- **Session Management**: User session tracking and data persistence
- **Analytics**: Popular stocks tracking and platform usage statistics
- **Performance Monitoring**: Watchlist performance tracking and historical analysis

### 4. User Interface
- **Search Interface**: Prominent stock symbol input with validation
- **Results Display**: Comprehensive company information presentation
- **Interactive Elements**: Primary action button for stock research
- **Theme**: Dark theme for professional appearance
- **Layout**: Seven-tab system for comprehensive analysis
- **Search Enhancement**: Company name and symbol search with intelligent suggestions

## Data Flow

1. **User Input**: Stock symbol entered through Streamlit text input
2. **Data Retrieval**: yfinance API call to fetch stock data
3. **Validation**: Check for valid stock symbol and data availability
4. **Processing**: Parallel execution of valuation and recommendation calculations
5. **Display**: Render results through Streamlit components with error handling

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **yfinance**: Yahoo Finance API wrapper
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization library
- **fredapi**: Federal Reserve Economic Data API access
- **requests**: HTTP library for web data retrieval

### Financial Data Sources
- **Yahoo Finance**: Primary data source for stock quotes, historical data, and company fundamentals
- **Federal Reserve Economic Data (FRED)**: Macroeconomic indicators (GDP, inflation, unemployment, interest rates)
- **Real-time Updates**: Live market data integration

## Deployment Strategy

### Local Development
- Streamlit development server with hot reload capability
- Page configuration optimized for wide layout and user experience

### Production Considerations
- The application is designed to be stateless for easy horizontal scaling
- Error handling implemented for API failures and data unavailability
- Modular architecture supports easy testing and maintenance

### Configuration
- Page settings configured for optimal user experience
- Custom page icon and title for branding
- Responsive design with column-based layout system
- Dark theme configuration for professional appearance

## Recent Changes (July 2025)

### Professional Services Integration
- Added professional research analyst contact information
- Integrated Manohar Mazumdar's credentials (NISM Certified Research Analyst)
- Added contact details and advisory pricing information
- Created professional services sidebar for user engagement
- Database functionality removed as per user request

### Macroeconomic Integration
- Added comprehensive macroeconomic analysis module
- Integrated GDP, inflation, unemployment, and interest rate data
- Sector-specific economic sensitivity analysis
- Economic impact visualization and downloadable reports

### User Interface Enhancements
- Implemented dark theme for professional equity research environment
- Added "Economic Impact" and "Profit Compounding" analysis tabs
- Enhanced search functionality to accept company names and stock symbols
- Added support for Indian stock markets (NSE/BSE exchanges)
- Implemented intelligent company name suggestions
- Added interactive sidebar with watchlist and dashboard features
- Fixed accessibility warnings and enhanced visual presentation

### Company Search Features
- Support for both US and Indian stock markets
- Intelligent name-to-symbol mapping for major companies
- Real-time search suggestions as users type
- Automatic exchange detection for Indian stocks (.NS/.BO suffixes)
- Partial name matching for improved user experience

### Profit Compounding Analysis
- Comprehensive analysis of company's profit reinvestment efficiency
- Revenue and profit growth trend analysis
- Return on Equity (ROE) tracking over multiple years
- Retained earnings growth evaluation
- Management efficiency indicators
- Visual growth trend analysis with quadrant mapping
- Scoring system for compounding quality assessment

### Data Persistence Features
- Automatic saving of all stock analyses to database
- Personal watchlist with performance tracking
- Search history with query type classification
- Popular stocks tracking across all users
- Platform usage statistics and analytics
- Downloadable watchlist and analysis reports

## Technical Notes

- The application uses a centered three-column layout for the main search interface
- Error handling is implemented for invalid stock symbols and missing data
- The valuation module includes fallback calculations when specific financial data is unavailable
- The recommendation system uses a scoring approach that can be easily extended with additional factors