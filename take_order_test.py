from API.config import Configg
from UTILS.calc_qnt import calc_qnt_func
import hmac 
import hashlib
import requests
import time
confg = Configg()
api_key = confg.api_key
api_secret = confg.api_secret

# print(api_key)
# print(api_secret)

def hashing(query_string):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def market_order(symbol, side, typee, price, qnt, timeinForce):
    url = 'https://testnet.binancefuture.com/fapi/v1/order' 
    # url = 'https://testnet.binance.vision/api/v3/order' 
    lo = 'BOTH'

    current_time = int(time.time() * 1000)
    query_string = f"symbol={symbol}&side={side}&positionside={lo}&type={typee}&quantity={qnt}&timestamp={current_time}"
    sing = hashing(query_string)
    query_string += f"&signature={sing}"

    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.post(url=url + '?' + query_string, headers=headers)
    print(response.text)



symbol = 'BTCUSDT'
side = 'BUY'
# typeee = 'LIMIT'
typeee = 'MARKET'
depo = 10000
price = 26776.0
timeInForce = 'GTC'

qnt, _ = calc_qnt_func(symbol, price, depo)

print(qnt)
price = 0.0
timeInForce = None
market_order(symbol, side, typeee, price, qnt, timeInForce)