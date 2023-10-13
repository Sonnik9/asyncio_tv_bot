import os
from dotenv import load_dotenv
from pparamss import my_params
import hmac 
import hashlib 
import requests
import time

load_dotenv()

class Configg():

    header = None

    def __init__(self) -> None:
        if not my_params.TEST_FLAG:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_REAL", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_REAL", "")
        else:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_FUTURES_TEST", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_FUTURES_TEST", "")

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }

    def get_signature(self, query_string):
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    
    def HTTP_request(self, url, **kwards):

        responce = None

        for _ in range(2):
            try:
                responce = requests.request(url=url, **kwards)
                responce = responce.json()  
                break
            except Exception as ex:
                time.sleep(2)
                print(f"Config_41str:  {ex}") 
                continue

        return responce

# python -m API.config
