from datetime import datetime
import logging
import shioaji as sj
import pandas as pd
from typing import List, Dict

"""
Taiwan stock market example target:
0050 元大台灣50
006208 富邦台50
2330 台積電
2454 聯發科
"""

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AutoTrader')

class Trading:
    """
    Including functions:
    - get_market_data
    - analyze_signal
    - execute_trade
    - manage_risk
    - trading_loop
    """
    def __init__(self, api, profile):
        self.api = api
        self.profile = profile
        self.market_data = pd.DataFrame()

    def get_market_data(self, symbol:List[str]) -> Dict[str, any]:
        """
        Fetch market data for given symbol from TSE

        Args:
            symbol: Stock code follow by specific exchange, ex. TSE2330

        Return of self.api.Contracts.Stocks[symbol]:
            Stock(
                exchange=<Exchange.TSE: 'TSE'>, 
                code='2890', 
                symbol='TSE2890', 
                name='永豐金', 
                category='17', 
                unit=1000, 
                limit_up=19.1, 
                limit_down=15.7, 
                reference=17.4, 
                update_date='2023/01/17', 
                day_trade=<DayTrade.Yes: 'Yes'>
            )

        Data format and corresponding label:
            exchange (Exchange): 交易所 {OES, OTC, TSE ...等}
            code (str): 商品代碼
            symbol (str): 符號
            name (str): 商品名稱
            category (str): 類別
            unit (int): 單位
            limit_up (float): 漲停價
            limit_down (float): 跌停價
            reference (float): 參考價
            update_date (str): 更新日期
            margin_trading_balance (int): 融資餘額
            short_selling_balance (int): 融券餘額
            day_trade (DayTrade): 可否當沖 {Yes, No, OnlyBuy}
        """
        market_data = {}

        for sym in symbol:
            try:
                quote = self.api.quote.subscribe(
                    self.api.Contracts.Stocks[sym],
                    quote_type = sj.constant.QuoteType.Quote,
                    version = sj.constant.QuoteVersion.v1
                )
                print(quote)
                contract = self.api.Contracts.Stocks[sym]
                data = pd.DataFrame({
                    'symbol': [sym],
                    'limit_up': [contract.limit_up],
                    'limit_down': [contract.limit_down],
                    'reference': [contract.reference],
                    'update_date': [contract.update_date],
                    'margin_trading_balance': [contract.margin_trading_balance],
                    'short_selling_balance': [contract.short_selling_balance]
                })
            except Exception as e:
                logger.error(f"Error fetching data for symbol {sym}: {e}")
        
            if not data.empty:
                try:
                    market_data[sym] = data
                except Exception as e:
                    logger.error(f"Error combining {sym} market data into dataframe: {e}")

        self.market_data = market_data
        return market_data

    
    def analyze_signal(self, symbol: str, strategy: str = 'default') -> Dict[str, any]:
        """
        Analyze trading signal for given symbol and strategy

        Args:
            default:
            ma_crossover:
            rsi:
        """

        if symbol not in self.market_data:
            logger.error(f"No market data available for {symbol}")
            return {'signal': 'none', 'strength': 0, 'reason': 'No data available'}
        
        data = self.market_data[symbol]
        return data
    
    def strategy_default(self) -> Dict[str, any]:
        """
        """
    
    def strategy_ma_crossover(self) -> Dict[str, any]:
        """
        """

    def strategy_rsi(self) -> Dict[str, any]:
        """
        """
    
    def execute_trade(self) -> Dict[str, any]:
        """
        """
    
    def sufficient_balance(self) -> Dict[str, any]:
        """
        """

    def sufficient_holdings(self) -> Dict[str, any]:
        """
        """
    
    def manage_risk(self) -> Dict[str, any]:
        """
        """
    
    def calculate_position_size(self) -> Dict[str, any]:
        """
        """
    
    def trading_loop(self) -> Dict[str, any]:
        """
        """

