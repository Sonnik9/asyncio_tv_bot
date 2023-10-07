from API.config import Configg
from pparamss import my_params

class CREATE_BINANCE_ORDER(Configg):

    def __init__(self, market, test_flag) -> None:
        super().__init__(market=market, test_flag=test_flag)

    def open_order(self, item, qnt):
        response = None

        if item["defender"] == 1:
            side = 'BUY'
        elif item["defender"] == -1:
            side = "SELL"

        params = {
            'symbol': item["symbol"],
            'quantity': qnt,
            'price': item["enter_price"],
            'side': side,  
            'type': 'MARKET',  
        }        
        
        if self.market == 'spot':
            response = self.spot_client.create_order(**params)
        elif self.market == 'futures':
            # response = self.futures_client.new_order(**params)
            response = self.spot_client.futures_create_order(**params)
        else:
            raise ValueError("Invalid market type")       

        return response

    def close_order(self, item):

        response = None

        if item["defender"] == 1:
            side = 'SELL'
        elif item["defender"] == -1:
            side = "BUY"

        params = {
            'symbol': item["symbol"],           
            'side': side,  
            'type': 'MARKET',  
        }        
        
        if self.market == 'spot':
            response = self.spot_client.create_order(**params)
        elif self.market == 'futures':
            # response = self.futures_client.new_order(**params)
            response = self.spot_client.futures_create_order(**params)
        else:
            raise ValueError("Invalid market type")       

        return response

    def cancel_all_orderss(self, symbol, order_id):
        response = None
        params = {
            'symbol': symbol,
            'orderId': order_id,
            'type': 'LIMIT', 
        }        
        
        if self.market == 'spot':
            response = self.spot_client.cancel_order(**params)
        elif self.market == 'futures':
            response = self.futures_client.cancel_order(**params)
        else:
            raise ValueError("Invalid market type")
        
        return response
    
create_orders_obj = CREATE_BINANCE_ORDER(market='spot', test_flag=False)


        