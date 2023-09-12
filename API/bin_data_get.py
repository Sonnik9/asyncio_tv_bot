from API.config import Configg
import time
from pparamss import my_params



class GET_BINANCE_DATA(Configg):

    def __init__(self, market, test_flag) -> None:
        super().__init__(market=market, test_flag=test_flag)
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
                        all_tickers = self.spot_client.get_ticker()
                        symbols = self.top_coins_filter(all_tickers, limit_selection_coins)
                    elif self.market == 'futures':
                        all_tickers = self.futures_client.ticker_24hr_price_change()
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
    
bin_data = GET_BINANCE_DATA(my_params.market, my_params.test_flag)
