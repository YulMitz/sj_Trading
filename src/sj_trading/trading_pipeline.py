import os
import shioaji as sj
from . import account, trader



def preview_market_data():
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=os.environ["API_KEY"],
        secret_key=os.environ["SECRET_KEY"],
        fetch_contract=True,
        contracts_timeout=10000
    )
    print("Simulation environment login success")

    Trader = trader.Trading(api, account.profile)
    test_symbols = ['2330', '2454']

    df = Trader.get_market_data(test_symbols)
    print(df)