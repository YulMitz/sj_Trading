import os
import shioaji as sj
from dotenv import load_dotenv

load_dotenv()
print(sj.__version__)

def main():
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=os.environ["API_KEY"],
        secret_key=os.environ["SECRET_KEY"],
        fetch_contract=False
    )
    print("login success")
