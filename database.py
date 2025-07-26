import os
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from typing import List, Dict, Optional

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class StockAnalysis(Base):
    __tablename__ = "stock_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    company_name = Column(String)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    current_price = Column(Float)
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    
    # Valuation data
    dcf_fair_value = Column(Float)
    pe_fair_value = Column(Float)
    
    # Recommendation
    recommendation_action = Column(String)
    recommendation_score = Column(Integer)
    recommendation_reason = Column(Text)
    
    # Economic indicators
    economic_sentiment = Column(String)
    gdp_growth = Column(Float)
    inflation_rate = Column(Float)
    unemployment_rate = Column(Float)
    fed_funds_rate = Column(Float)
    
    # Compounding analysis
    compounding_score = Column(Integer)
    is_compounding = Column(Boolean)
    revenue_growth = Column(Float)
    profit_growth = Column(Float)
    roe_trend = Column(Float)
    
    # Raw analysis data (JSON)
    full_analysis = Column(JSON)

class UserWatchlist(Base):
    __tablename__ = "user_watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Can be session-based or user-based
    symbol = Column(String, index=True)
    company_name = Column(String)
    added_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    alert_price = Column(Float)
    is_active = Column(Boolean, default=True)

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    search_query = Column(String)
    resolved_symbol = Column(String)
    search_date = Column(DateTime, default=datetime.utcnow)
    search_type = Column(String)  # 'symbol' or 'company_name'

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def save_stock_analysis(self, symbol: str, company_name: str, analysis_data: Dict):
        """Save complete stock analysis to database"""
        session = self.get_session()
        try:
            # Extract key data from analysis
            info = analysis_data.get('info', {})
            valuation = analysis_data.get('valuation', {})
            recommendation = analysis_data.get('recommendation', {})
            economic = analysis_data.get('economic', {})
            compounding = analysis_data.get('compounding', {})
            
            analysis = StockAnalysis(
                symbol=symbol,
                company_name=company_name,
                current_price=info.get('currentPrice'),
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield'),
                
                dcf_fair_value=valuation.get('dcf_value'),
                pe_fair_value=valuation.get('pe_value'),
                
                recommendation_action=recommendation.get('action'),
                recommendation_score=recommendation.get('score'),
                recommendation_reason=recommendation.get('reason'),
                
                economic_sentiment=economic.get('overall_sentiment'),
                gdp_growth=economic.get('gdp_growth'),
                inflation_rate=economic.get('inflation_rate'),
                unemployment_rate=economic.get('unemployment_rate'),
                fed_funds_rate=economic.get('fed_funds_rate'),
                
                compounding_score=compounding.get('compounding_score'),
                is_compounding=compounding.get('is_compounding'),
                revenue_growth=compounding.get('revenue_growth'),
                profit_growth=compounding.get('profit_growth'),
                roe_trend=compounding.get('roe_trend'),
                
                full_analysis=analysis_data
            )
            
            session.add(analysis)
            session.commit()
            return analysis.id
        except Exception as e:
            session.rollback()
            print(f"Error saving analysis: {e}")
            return None
        finally:
            session.close()
    
    def get_stock_analysis_history(self, symbol: str, limit: int = 10):
        """Get historical analyses for a stock"""
        session = self.get_session()
        try:
            analyses = session.query(StockAnalysis).filter(
                StockAnalysis.symbol == symbol
            ).order_by(StockAnalysis.analysis_date.desc()).limit(limit).all()
            return analyses
        except Exception as e:
            print(f"Error retrieving analysis history: {e}")
            return []
        finally:
            session.close()
    
    def add_to_watchlist(self, user_id: str, symbol: str, company_name: str, notes: str = "", alert_price: float = None):
        """Add stock to user's watchlist"""
        session = self.get_session()
        try:
            # Check if already in watchlist
            existing = session.query(UserWatchlist).filter(
                UserWatchlist.user_id == user_id,
                UserWatchlist.symbol == symbol,
                UserWatchlist.is_active == True
            ).first()
            
            if existing:
                return False, "Stock already in watchlist"
            
            watchlist_item = UserWatchlist(
                user_id=user_id,
                symbol=symbol,
                company_name=company_name,
                notes=notes,
                alert_price=alert_price if alert_price is not None else None
            )
            
            session.add(watchlist_item)
            session.commit()
            return True, "Added to watchlist successfully"
        except Exception as e:
            session.rollback()
            print(f"Error adding to watchlist: {e}")
            return False, str(e)
        finally:
            session.close()
    
    def get_user_watchlist(self, user_id: str):
        """Get user's active watchlist"""
        session = self.get_session()
        try:
            watchlist = session.query(UserWatchlist).filter(
                UserWatchlist.user_id == user_id,
                UserWatchlist.is_active == True
            ).order_by(UserWatchlist.added_date.desc()).all()
            return watchlist
        except Exception as e:
            print(f"Error retrieving watchlist: {e}")
            return []
        finally:
            session.close()
    
    def remove_from_watchlist(self, user_id: str, symbol: str):
        """Remove stock from watchlist"""
        session = self.get_session()
        try:
            watchlist_item = session.query(UserWatchlist).filter(
                UserWatchlist.user_id == user_id,
                UserWatchlist.symbol == symbol
            ).first()
            
            if watchlist_item:
                session.delete(watchlist_item)
                session.commit()
                return True, "Removed from watchlist"
            else:
                return False, "Stock not found in watchlist"
        except Exception as e:
            session.rollback()
            print(f"Error removing from watchlist: {e}")
            return False, str(e)
        finally:
            session.close()
    
    def save_search_history(self, user_id: str, search_query: str, resolved_symbol: str, search_type: str):
        """Save user search history"""
        session = self.get_session()
        try:
            search_record = SearchHistory(
                user_id=user_id,
                search_query=search_query,
                resolved_symbol=resolved_symbol,
                search_type=search_type
            )
            
            session.add(search_record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving search history: {e}")
        finally:
            session.close()
    
    def get_search_history(self, user_id: str, limit: int = 20):
        """Get user's search history"""
        session = self.get_session()
        try:
            history = session.query(SearchHistory).filter(
                SearchHistory.user_id == user_id
            ).order_by(SearchHistory.search_date.desc()).limit(limit).all()
            return history
        except Exception as e:
            print(f"Error retrieving search history: {e}")
            return []
        finally:
            session.close()
    
    def get_popular_stocks(self, limit: int = 10):
        """Get most analyzed stocks"""
        session = self.get_session()
        try:
            from sqlalchemy import func
            popular = session.query(
                StockAnalysis.symbol,
                StockAnalysis.company_name,
                func.count(StockAnalysis.id).label('analysis_count'),
                func.max(StockAnalysis.analysis_date).label('last_analysis')
            ).group_by(
                StockAnalysis.symbol,
                StockAnalysis.company_name
            ).order_by(
                func.count(StockAnalysis.id).desc()
            ).limit(limit).all()
            
            return popular
        except Exception as e:
            print(f"Error retrieving popular stocks: {e}")
            return []
        finally:
            session.close()
    
    def get_recent_analyses(self, limit: int = 10):
        """Get recent stock analyses across all users"""
        session = self.get_session()
        try:
            recent = session.query(StockAnalysis).order_by(
                StockAnalysis.analysis_date.desc()
            ).limit(limit).all()
            return recent
        except Exception as e:
            print(f"Error retrieving recent analyses: {e}")
            return []
        finally:
            session.close()
    
    def get_watchlist_performance(self, user_id: str):
        """Get performance data for user's watchlist"""
        session = self.get_session()
        try:
            watchlist = self.get_user_watchlist(user_id)
            performance_data = []
            
            for item in watchlist:
                # Get latest analysis for each stock
                latest_analysis = session.query(StockAnalysis).filter(
                    StockAnalysis.symbol == item.symbol
                ).order_by(StockAnalysis.analysis_date.desc()).first()
                
                if latest_analysis:
                    performance_data.append({
                        'symbol': item.symbol,
                        'company_name': item.company_name,
                        'added_date': item.added_date,
                        'current_price': latest_analysis.current_price,
                        'recommendation': latest_analysis.recommendation_action,
                        'compounding_score': latest_analysis.compounding_score,
                        'alert_price': item.alert_price,
                        'notes': item.notes
                    })
            
            return performance_data
        except Exception as e:
            print(f"Error retrieving watchlist performance: {e}")
            return []
        finally:
            session.close()

# Initialize database manager
db_manager = DatabaseManager()