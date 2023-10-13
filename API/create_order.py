from API.config import Configg
from pparamss import my_params
import time

class CREATE_BINANCE_ORDER(Configg):

    def __init__(self) -> None:
        super().__init__()

    def make_order(self, item, qnt, is_closing):

        response = None
        url = my_params.URL_PATTERN_DICT['create_order_url']
        method = 'POST'
        typee = 'MARKET'
        symbol = item["symbol"]       

        if item["defender"] == 1*is_closing:
            side = 'BUY'
        elif item["defender"] == -1*is_closing:
            side = "SELL" 

        current_time = int(time.time() * 1000)
        query_string = f"symbol={symbol}&side={side}&type={typee}&quantity={qnt}&timestamp={current_time}"
        sing = self.get_signature(query_string)
        query_string += f"&signature={sing}"
        req_url = url + '?' + query_string

        response = self.HTTP_request(req_url, method=method, headers=self.header)
        
        return response
    
    def cancel_all_orders(self):
        
        response = None
        method = 'DELETE'
        req_url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
        response = self.HTTP_request(req_url, method=method, headers=self.header)
        
        return response
        
create_orders_obj = CREATE_BINANCE_ORDER()
