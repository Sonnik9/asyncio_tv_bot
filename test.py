# usdt_filtered = [9,3,7,2,5]
# data_list = sorted(usdt_filtered, key=lambda x: x, reverse=True)
# print(data_list)

from binance.client import Client

api_key = ''
api_secret = ''

spot_client = Client(api_key, api_secret)

print(spot_client)