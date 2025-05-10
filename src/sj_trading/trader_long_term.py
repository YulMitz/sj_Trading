from datetime import datetime, timedelta
import time
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
        Fetch quote market data for given symbol from TSE

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

        now = datetime.now()
        weekday = now.weekday()
        hour = now.hour
        minute = now.minute
        simulation = False

        # If not in market time or not in trading day, simulate transaction by historical ticks
        if weekday >= 5:
            logger.info(f"Today is not trading day")
            match weekday:
                case 5:
                    nearest_trading_day = now - timedelta(days=1)
                case 6:
                    nearest_trading_day = now - timedelta(days=2)
            simulation = True

        if weekday < 5 and (hour <= 9 or hour >= 13):
            if (hour == 9 and minute < 30) or (hour == 13 and minute > 30):
                logger.info(f"Trading day, but market is closed")
                nearest_trading_day = now - timedelta(days=1)
                simulation = True

        for sym in symbol:
            try:
                contract = self.api.Contracts.Stocks[sym]

                if simulation:
                    logger.info(f"Simulate transaction by historical ticks for {sym}")
                    # Get historical ticks data
                    ticks = self.api.ticks(contract = contract, date = nearest_trading_day.strftime("%Y-%m-%d"))
                    data = pd.DataFrame({**ticks})
                    data.ts = pd.to_datetime(data.ts)
                else:
                    # Get real-time tick data
                    Tick = self.api.quote.subscribe(
                        contract,
                        quote_type=sj.constant.QuoteType.Tick,
                        version=sj.constant.QuoteVersion.v1,
                        intraday_odd=True
                    )
                    
                    # Timeout machinism while trading
                    start_time = time.time()
                    timeout = 30
                    
                    while Tick is None:
                        logger.info(f"Waiting for real-time tick data for {sym}")
                        time.sleep(0.5)

                        if time.time() - start_time > timeout:
                            logger.error(f"Timeout waiting for real-time tick data for {sym}")
                            break

                    logger.info(f"Real-time tick data for {sym} has been received")

                    data = pd.DataFrame({**Tick})
            except Exception as e:
                logger.error(f"Error fetching data for symbol {sym}: {e}")
        
            if not data.empty:
                try:
                    market_data[sym] = data
                    logger.info(f"{sym} has been read in market data")
                except Exception as e:
                    logger.error(f"Error combining {sym} market data into dataframe: {e}")

        self.market_data = market_data
        return market_data

    
    def analyze_signal(self, symbol: str, strategy: str = 'default') -> Dict[str, any]:
        """
        Analyze trading signal for given symbol and strategy

        Args:
            default: SMA-20
            ma_crossover:
            rsi:
        """

        if symbol not in self.market_data:
            logger.error(f"No market data available for {symbol}")
            return {'signal': 'none', 'strength': 0, 'reason': 'No data available'}
        
        # Get market data for signal calculation
        data = self.market_data[symbol]

        match strategy:
            case 'default':
                signal = self.strategy_default(data)
            case 'ma_crossover':
                signal = self.strategy_ma_crossover(data)
            case 'rsi':
                signal = self.strategy_rsi(data)
            case _:
                logger.error(f"Unknown strategy: {strategy}")
                return {'signal': 'none', 'strength': 0, 'reason': 'Unknown strategy'}

        return signal
    
    def strategy_default(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Default strategy: SMA-20

        Args:
            df: Dataframe of real-time tick data
        """

        df['SMA-20'] = df['close'].rolling(window=20).mean()
        df['SMA-diff'] = df['close'] - df['SMA-20']
        df['SMA-lag-diff'] = df['SMA-diff'].shift(periods=1)

        return df
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