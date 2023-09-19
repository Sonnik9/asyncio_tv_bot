import os
from dotenv import load_dotenv

from binance.client import Client
from binance.um_futures import UMFutures
import hmac 
import hashlib 
import requests
# pip install python-dotenv

load_dotenv()

class Configg():

    api_key, api_secret = None, None
    spot_client, futures_client = None, None
    header = None

    def __init__(self, market, test_flag) -> None:  
        if market == 'spot':
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_SPOT", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_SPOT", "")
            self.spot_client = Client(self.api_key, self.api_secret)
        if market == 'futures':
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_FUTURES", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_FUTURES", "")  
            self.futures_client = UMFutures(self.api_key, self.api_secret)
             
        self.market = market    
        self.test_flag = test_flag

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }

    def get_signature(self, params):
        import time
        params['timestamp'] = int(time.time() *1000)
        params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
        hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
        params['signature'] = hash.hexdigest()
        
        return params
    
    def HTTP_request(self, url, **kwards):
        responce = None
        try:
            responce = requests.request(url=url, **kwards)
            responce = responce.json()  
        except Exception as ex:
            print(ex) 
        # print(responce.status_code)
        # print(responce.json())
        return responce

# python -m API.config