from API.config import Configg
import time
from pparamss import my_params
import pandas as pd

class GET_BINANCE_DATA(Configg):

    def __init__(self, market, test_flag) -> None:
        super().__init__(market=market, test_flag=test_flag)
        # print(f"bin_data_10:__{self.binance_python_client}")
        # self.top_coins = []

    def top_coins_filter(self, all_tickers, limit_selection_coins):

        data_list = []
        top_data_list = []
        top_coins = [] 
        if not self.test_flag:  
            usdt_filtered = [ticker for ticker in all_tickers if 'USDT' in ticker['symbol'].upper() and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper()]
            data_list = sorted(usdt_filtered, key=lambda x: float(x['priceChangePercent']), reverse=True)
            if len(data_list) > limit_selection_coins:
                top_data_list = data_list[:limit_selection_coins]
            top_coins = [coins['symbol'] for coins in top_data_list]
        else:
            top_coins = [ticker for ticker in all_tickers if 'USDT' in ticker.upper() and 'UP' not in ticker.upper() and 'DOWN' not in ticker.upper()]

            if len(top_coins) > limit_selection_coins:
                top_coins = top_coins[:limit_selection_coins]

        # self.top_coins = top_coins
        return top_coins

    def all_tickers_func(self, limit_selection_coins):
        symbols = []
        all_tickers = None
        method = 'GET'
        params = {}
        if not self.test_flag:
            for _ in range(3):
                try:
                    if self.market == 'spot':
                        all_tickers = self.binance_python_client.get_ticker()                        
                        symbols = self.top_coins_filter(all_tickers, limit_selection_coins)
                    elif self.market == 'futures':
                        all_tickers = self.binance_python_client.futures_ticker()                      
                        symbols = self.top_coins_filter(all_tickers, limit_selection_coins)
                    break
                except Exception as ex:
                    print(f"API/get_data_26:___{ex}")  
                    time.sleep(2)
                    continue
        else:
            if self.market == 'spot':           
                url = 'https://testnet.binance.vision/api/v3/exchangeInfo'
            elif self.market == 'futures':      
                url = 'https://testnet.binancefuture.com/fapi/v1/exchangeInfo'
                try:
                    params = self.get_signature(params)
                except Exception as ex:
                    print(ex)
            try:                
                all_tickers = self.HTTP_request(url, method=method, headers=self.header, params=params)                
                symbols = [symbol['symbol'] for symbol in all_tickers['symbols']]
                symbols = self.top_coins_filter(symbols, limit_selection_coins)
            except Exception as ex:
                print(ex)
        
        return symbols
    
    def get_klines_helper(self, symbol):
        klines = None
        data = None
      
        for _ in range(3):
            try:
                if self.market == 'spot':                    
                    klines = self.binance_python_client.get_klines(symbol=symbol, interval=my_params.interval, limit=50)
                elif self.market == 'futures':
                    klines = self.binance_python_client.futures_klines(symbol=symbol, interval=my_params.interval, limit=50)
                time.sleep(0.1)
                break
            except Exception as ex:
                print(f"API/get_data_13:___{ex}")
                time.sleep(2)
                continue  

        if klines:
            data = pd.DataFrame(klines).iloc[:, :6]
            data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            data = data.set_index('Time')
            data.index = pd.to_datetime(data.index, unit='ms')
            data = data.astype(float)
            
        return data
    
    def get_klines(self, data):

        for item in data:
            symbol = item["symbol"]
            item["klines"] = self.get_klines_helper(symbol)
        return data
    
# python -m API.get_data
   
bin_data = GET_BINANCE_DATA(my_params.market, my_params.test_flag)
