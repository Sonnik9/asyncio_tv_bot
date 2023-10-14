from pparamss import my_params
# usdt_filtered = [9,3,7,2,5]
# data_list = sorted(usdt_filtered, key=lambda x: x, reverse=True)
# print(data_list)

# from binance.client import Client

# api_key = ''
# api_secret = ''

# spot_client = Client(api_key, api_secret)

# print(spot_client)

# from itertools import accumulate

# results = [10, -50, 8, -2, 15, -10, 5]
# cash_flows = list(accumulate(results))
# min_drawdown = min(cash_flows)
# max_flow_profit = max(cash_flows)

# print(f"Минимальная просадка: {min_drawdown}")
# print(f"Максимальный профит: {max_flow_profit}")

# from API.config import Configg

# conf = Configg()

# # Получите информацию о фьючерсных позициях
# balans = conf.binance_python_client.futures_account_balance()
# # print(balans)

# for bal in balans:
#     if bal["asset"] == 'USDT':
#         print(f'{bal["asset"]}: {bal["balance"]}')

# positions = conf.binance_python_client.futures_account()
# # print(positions)

# # Ликвидация всех открытых позиций
# for position in positions['positions']:
#     symbol = position['symbol']
#     if float(position['positionAmt']) != 0:
#         response = conf.binance_python_client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=abs(float(position['positionAmt'])))
#         print(f"Ликвидирована позиция: {symbol}")


# import base64
# import requests
# import time
# from cryptography.hazmat.primitives.serialization import load_pem_private_key

# from API.config import Configg
# from UTILS.calc_qnt import calc_qnt_func

# conf = Configg()

# # Set up authentication
# API_KEY = conf.api_key
# PRIVATE_KEY_PATH = conf.api_secret
# private_key = PRIVATE_KEY_PATH

# # Load the private key.
# # In this example the key is expected to be stored without encryption,
# # but we recommend using a strong password for improved security.
# # with open(PRIVATE_KEY_PATH, 'rb') as f:
# #     private_key = load_pem_private_key(data=f.read(),
# #                                        password=None)
    
# depo = 20
# price = 14.930
# symbol = 'ETCUSDT'
# qnt = calc_qnt_func(symbol, price, depo)

# # print(str(qnt))
# params = {
#     'symbol':       symbol,
#     'side':         'SELL',
#     'type':         'MARKET',
#     'timeInForce':  'GTC',
#     'quantity':     qnt,
#     'price':        price,
# }

# # Set up the request parameters
# # params = {
# #     'symbol':       'BTCUSDT',
# #     'side':         'SELL',
# #     'type':         'LIMIT',
# #     'timeInForce':  'GTC',
# #     'quantity':     '1.0000000',
# #     'price':        '0.20',
# # }

# # Timestamp the request
# timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
# params['timestamp'] = timestamp

# # Sign the request
# payload = '&'.join([f'{param}={value}' for param, value in params.items()])
# signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
# params['signature'] = signature

# # Send the request
# headers = {
#     'X-MBX-APIKEY': API_KEY,
# }
# url = 'https://testnet.binancefuture.com/fapi/v1/order' 
# # url = 'https://testnet.binance.vision/api/v3/order' 
# response = requests.post(
#     url,
#     headers=headers,
#     data=params,
# )
# print(response.json())

# a=[1,2,3,4,5,7]
# print(len(a))

# for item in a:
#     if item == 2:
#         a.remove(item)
# print(len(a))
# usdt_filtered = [78,1,45, 100]
# usdt_filtered = usdt_filtered[:3]
# print(usdt_filtered)
# data_list = sorted(usdt_filtered, key=lambda x: x, reverse=True)
# print(data_list)


# from binance.client import Client
# import requests

# api_key = ''
# api_secret = ''

# client = Client(api_key, api_secret, testnet=True)

# def filter_top_pairs(url, volume_limit, price_change_limit):
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()

#         all_pairs = [ticker for ticker in data if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper()]
#         exchange_info = client.futures_exchange_info()
#         # exchange_info = client.get_exchange_info()

#         print(len(all_pairs))

#         crypto_pairs = [pair["symbol"] for pair in exchange_info['symbols'] if pair['symbol'].endswith('USDT')]
#         print(len(crypto_pairs))

#         crypto_pairs = [x for x in  all_pairs if x["symbol"] in crypto_pairs]
        
#         sorted_by_volume = sorted(crypto_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
#         top_pairs_by_volume = sorted_by_volume[:volume_limit]
#         return [pair['symbol'] for pair in top_pairs_by_volume]

#         # sorted_by_price_change = sorted(top_pairs_by_volume, key=lambda x: float(x['priceChangePercent']), reverse=True)
#         # top_pairs = sorted_by_price_change[:price_change_limit]

#         return [pair['symbol'] for pair in top_pairs]

#     else:
#         print("Ошибка при запросе к API")
#         return []

# # URL для получения информации о парам с биржи Binance

# url = "https://api.binance.com/api/v3/ticker/24hr"
# url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
# url = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"

# # Установка лимитов
# volume_limit = 40  # Лимит по объему пар
# price_change_limit = 30  # Лимит по процентному изменению цены


# # Получение списка отфильтрованных пар
# filtered_pairs = filter_top_pairs(url, volume_limit, price_change_limit)

# print(filtered_pairs)




# def top_coins_filter(self, all_tickers):
    
#     top_coins_pairs = []
#     usdt_filtered = [] 
#     volume_filtered = []
#     price_changing_filtered = [] 
#     # print(len(all_tickers)) 
#     usdt_filtered = [ticker for ticker in all_tickers if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper()]
#     # usdt_filtered = usdt_filtered[:10]
#     # print(usdt_filtered[:1])
#     # hcc = [coins['symbol'] for coins in usdt_filtered]
#     # print(hcc[:10])
#     volume_filtered = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)
#     volume_filtered = volume_filtered[:my_params.slice_volume_pairs]
#     volume_filtered = [coins['symbol'] for coins in volume_filtered]
#     return volume_filtered
#     # print(hc)
#     # price_changing_filtered = sorted(volume_filtered, key=lambda x: float(x['priceChangePercent']), reverse=True)        
#     # top_coins_pairs = price_changing_filtered[:my_params.slice_priceChanging_pairs]
#     # top_coins_pairs = [coins['symbol'] for coins in top_coins_pairs]

#     # return top_coins_pairs

# import requests

# def get_top_pairs():
#     if not my_params.test_flag:
#         url = "https://api.binance.com/api/v3/ticker/24hr"
#         url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
#     else:
#         if my_params.market == 'spot':
#             url = "https://testnet.binance.com/v3/ticker/24hr"
#         else:
#             url = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"

#     all_tickers = []
#     top_pairs = []
#     sorted_by_volume_data = []
#     sorted_by_changing_price_data = []

#     response = requests.get(url)
#     if response.status_code == 200:
#         all_tickers = response.json()
#         print(len(all_tickers))

#         usdt_filtered = [ticker for ticker in all_tickers if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper() and 'EUR' not in ticker['symbol'].upper()]
        
#         sorted_by_volume_data = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)

#         sorted_by_volume_data = sorted_by_volume_data[:my_params.slice_volume_pairs]

#         sorted_by_changing_price_data = sorted(sorted_by_volume_data, key=lambda x: float(x['priceChangePercent']), reverse=True)
 
#         sorted_by_changing_price_data = sorted_by_changing_price_data[:my_params.slice_priceChanging_pairs]

#         top_pairs = [coins['symbol'] for coins in sorted_by_changing_price_data]

#         return top_pairs
#     else:
#         print("Ошибка при запросе к API")
#         return []

# top_pairs = get_top_pairs()
# print(len(top_pairs))
# print(top_pairs)

# from API.config import Configg
# import time
# from pparamss import my_params
# import pandas as pd

# class GET_BINANCE_DATA(Configg):

#     def __init__(self) -> None:
#         super().__init__()

#     def top_coins_filter(self, all_tickers):
#         print(len(all_tickers))      
#         top_coins_pairs = []
#         usdt_filtered = [] 
#         volume_filtered = []
#         price_changing_filtered = [] 
#         # print(len(all_tickers)) 
#         usdt_filtered = [ticker for ticker in all_tickers if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper() and 'EUR' not in ticker['symbol'].upper()]
#         volume_filtered = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)
#         volume_filtered = volume_filtered[:my_params.slice_volume_pairs]
#         price_changing_filtered = sorted(volume_filtered, key=lambda x: float(x['priceChangePercent']), reverse=True)        
#         top_coins_pairs = price_changing_filtered[:my_params.slice_priceChanging_pairs]
#         top_coins_pairs = [coins['symbol'] for coins in top_coins_pairs]

#         return top_coins_pairs

#     def all_tickers_func(self):
#         symbols = []
#         all_tickers = None
        
#         for _ in range(2):
#             try:
#                 if my_params.market == 'spot':                    
#                     all_tickers = self.binance_python_client.get_ticker()                                         
#                     symbols = self.top_coins_filter(all_tickers)
#                 elif my_params.market == 'futures':
#                     all_tickers = self.binance_python_client.futures_ticker()                                     
#                     symbols = self.top_coins_filter(all_tickers)
#                 break
#             except Exception as ex:
#                 print(f"API/get_data_26:___{ex}")  
#                 time.sleep(2)
#                 continue

        
#         return symbols

    
# # python -m API.get_data
   
# bin_data = GET_BINANCE_DATA()

# top_coins_pairs = bin_data.all_tickers_func()
# print(len(top_coins_pairs))
# print(top_coins_pairs)

# b = abs(0)
# a = 9
# c = a / b

# print(c)
# open_order = {}
# open_order['stat'] = None

# if open_order and 'status' in open_order and open_order['status'] == 'NEW':
#     print('ok')
# else:
#     print(' not ok')

from API.config import Configg
# from UTILS.calc_qnt import calc_qnt_func
# import hmac 
# import hashlib
# import requests
# import time
# confg = Configg()
# api_key = confg.api_key
# api_secret = confg.api_secret

# # print(api_key)
# # print(api_secret)

# def hashing(query_string):
#     return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# def market_order(symbol, side, typee, price, qnt, timeinForce):
#     url = 'https://testnet.binancefuture.com/fapi/v1/order' 
#     # url = 'https://testnet.binance.vision/api/v3/order' 
#     lo = 'BOTH'

#     current_time = int(time.time() * 1000)
#     query_string = f"symbol={symbol}&side={side}&positionside={lo}&type={typee}&quantity={qnt}&timestamp={current_time}"
#     sing = hashing(query_string)
#     query_string += f"&signature={sing}"

#     headers = {
#         "X-MBX-APIKEY": api_key
#     }

#     response = requests.post(url=url + '?' + query_string, headers=headers)
#     print(response.text)



# symbol = 'BTCUSDT'
# side = 'BUY'
# # typeee = 'LIMIT'
# typeee = 'MARKET'
# depo = 10000
# price = 26776.0
# timeInForce = 'GTC'

# qnt, _ = calc_qnt_func(symbol, price, depo)

# print(qnt)
# price = 0.0
# timeInForce = None
# market_order(symbol, side, typeee, price, qnt, timeInForce)

# import requests
# import time
# import hmac
# import hashlib

# # Замените на свои данные
# api_key = 'YOUR_API_KEY'
# api_secret = 'YOUR_API_SECRET'
# base_url = 'https://testnet.binancefuture.com'

# # Функция для создания сигнатуры
# def generate_signature(query_string):
#     return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# # Получение временной метки
# current_time = int(time.time() * 1000)

# # Создание запроса для получения списка всех открытых ордеров
# open_orders_url = f"{base_url}/fapi/v1/allOpenOrders"
# query_string = f"timestamp={current_time}"
# signature = generate_signature(query_string)
# query_string += f"&signature={signature}"
# headers = {
#     'X-MBX-APIKEY': api_key,
# }
# response = requests.get(open_orders_url, headers=headers, params=query_string)
# open_orders = response.json()

# # Получение информации о позициях
# positions_url = f"{base_url}/fapi/v1/positionRisk"
# query_string = f"timestamp={current_time}"
# signature = generate_signature(query_string)
# query_string += f"&signature={signature}"
# response = requests.get(positions_url, headers=headers, params=query_string)
# positions = response.json()


import requests
import hashlib
import hmac
import time

# Замените на свои данные
api_key = '96f214ce691b0dd8fc65b23002ee4e5ce0b55684598645c2eb2d0a819a6d387a'
api_secret = '46e1372c84151cd7d486a4734cc21023ba1724d067b5967ce48ce769025cf0d2'
base_url = 'https://testnet.binancefuture.com'  # Используйте нужный URL

# Получение временной метки
timestamp = int(time.time() * 1000)

# Создание подписи
signature = hmac.new(api_secret.encode('utf-8'), f"timestamp={timestamp}".encode('utf-8'), hashlib.sha256).hexdigest()

# Получение всех позиций
headers = {
    'X-MBX-APIKEY': api_key
}
params = {
    'timestamp': timestamp,
    'signature': signature
}
positions_url = f"{base_url}/fapi/v2/positionRisk"
response = requests.get(positions_url, headers=headers, params=params)
positions = response.json()
# positions = positions
# print(positions)


# Закрытие всех позиций
for position in positions:
    if position['symbol'] == 'ATOMUSDT':
        print(position)
        if float(position['positionAmt']) != 0:
            symbol = position['symbol']
            position_side = position['positionSide']  # Определение направления позиции
            if position_side == "LONG":
                order_side = "SELL"  # Для LONG-позиции продаем
            else:
                order_side = "BUY"  # Для SHORT-позиции покупаем
            # Создание рыночного ордера
            order_params = {
                'symbol': symbol,
                'side': order_side,
                'type': 'MARKET',
                'quantity': abs(float(position['positionAmt']))
            }
            order_url = f"{base_url}/fapi/v1/order"
            response = requests.post(order_url, headers=headers, params=params, json=order_params)
            print(response)
            # print(f"Ликвидирована позиция: {symbol}")

    # print("Все открытые позиции закрыты.")
