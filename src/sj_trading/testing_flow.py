import os
import json
import shioaji as sj
from sj_trading import account, trader_long_term
from shioaji.constant import Action, StockPriceType, OrderType

def login():
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=os.environ["API_KEY"],
        secret_key=os.environ["SECRET_KEY"],
        fetch_contract=True,
        contracts_timeout=10000
    )
    print("Simulation environment login success")
    return api

def test_market_data():
    api = login()
    Trader = trader_long_term.Trading(api, account.profile)
    test_symbols = ['2330', '2454']

    Trader.get_market_data(test_symbols)
    Trader.analyze_signal(symbol='2330')

def test_stock_ordering():
    # 測試環境登入
    api = login()

    # 設定預設帳號
    api.set_default_account(api.stock_account)
    print(f"Default Account: {api.stock_account}")

    # 準備下單的 Contract
    # 使用 2890 永豐金為例
    contract = api.Contracts.Stocks["2890"]
    print(f"Contract: {contract}")

    # 建立委託下單的 Order
    order = sj.order.StockOrder(
        action=Action.Buy, # 買進
        price=contract.reference, # 以平盤價買進
        quantity=1, # 下單數量
        price_type=StockPriceType.LMT, # 限價單
        order_type=OrderType.ROD, # 當日有效單
        account=api.stock_account, # 使用預設的帳戶
    )
    print(f"Order: {order}")

    # 送出委託單
    trade = api.place_order(contract=contract, order=order)
    print(f"Trade: {trade}")

    # 更新狀態
    api.update_status()
    print(f"Status: {trade.status}")