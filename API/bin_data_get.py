from API.config import Configg
import requests
from pparamss import my_params

class GET_BINANCE_DATA(Configg):

    def __init__(self) -> None:
        super().__init__()   

    def get_top_pairs(self):
        url = my_params.URL_PATTERN_DICT['all_tikers_url']
        all_tickers = []
        top_pairs = []
        sorted_by_volume_data = []
        sorted_by_changing_price_data = []

        response = requests.get(url)

        if response.status_code == 200:
            all_tickers = response.json()
            # print(len(all_tickers))
            # print(all_tickers[0]['lastPrice'])
            usdt_filtered = [ticker for ticker in all_tickers if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper() and 'EUR' not in ticker['symbol'].upper() and float(ticker['lastPrice']) >= 1.0]
            
            sorted_by_volume_data = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)

            sorted_by_volume_data = sorted_by_volume_data[:my_params.SLICE_VOLUME_PAIRS]

            sorted_by_changing_price_data = sorted(sorted_by_volume_data, key=lambda x: float(x['priceChangePercent']), reverse=True)
    
            sorted_by_changing_price_data = sorted_by_changing_price_data[:my_params.SLICE_CHANGINGPRICES_PAIRS]

            top_pairs = [coins['symbol'] for coins in sorted_by_changing_price_data]

        return top_pairs
    
# python -m API.get_data
   
bin_data = GET_BINANCE_DATA()
