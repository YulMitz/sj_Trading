from datetime import datetime
import logging
import pandas as pd
from typing import List, Dict

"""
Taiwan stock market example target:
0050 元大台灣50
006208 富邦台50
2330 台積電
2454 聯發科
"""

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

    def get_market_data(self, symbol:List[str]) -> pd.DataFrame:
        """
        Fetch market data from specific stock code, it should return something like:
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

        Data format and corresponding meaning:
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

        symbol: Stock code follow by specific exchange, ex. TSE2330
        """
        market_data = []

        for sym in symbol:
            try:
                contract = self.api.Contracts.Stocks[sym]
                market_data.append({
                    'symbol': sym,
                    'limit_up': contract.limit_up,
                    'limit_down': contract.limit_down,
                    'reference': contract.reference,
                    'contract_info': contract
                })
            except Exception as e:
                print(f"Error fetching data for symbol {sym}: {e}")
        
        if market_data:
            try:
                df = pd.DataFrame(market_data)
            except Exception as e:
                print(f"Error combining market data into dataframe: {e}")

        return df

    
    def analyze_signal(self) -> Dict[str, any]:
        """
        """
    
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

