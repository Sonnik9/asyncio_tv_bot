from API.config import Configg
from pparamss import my_params

class CREATE_BINANCE_ORDER(Configg):

    def __init__(self, market, test_flag) -> None:
        super().__init__(market=market, test_flag=test_flag)

    def orders_request(self, **params):
        responce = None

        for _ in range(3):
            if self.market == 'spot':
                try:
                    responce = self.binance_python_client.create_order(**params)
                except Exception as ex:
                    print(ex)
                if responce:
                    break
            elif self.market == 'futures':   
                try:         
                    responce = self.binance_python_client.futures_create_order(**params) 
                except Exception as ex:
                    print(ex)                    
                if responce:
                    break

        return responce

    def open_order(self, item, qnt):
        responce = None

        if item["defender"] == 1:
            side = 'BUY'
        elif item["defender"] == -1:
            side = "SELL"

        params = {
            'symbol': item["symbol"],
            'quantity': qnt,
            'price': item["enter_price"],
            'side': side,  
            'type': 'MARKET'
        }  

        responce = self.orders_request(**params)  
        return responce      

    def close_order(self, item):
        responce = None

        if item["defender"] == 1:
            side = 'SELL'
        elif item["defender"] == -1:
            side = "BUY"

        params = {
            'symbol': item["symbol"],           
            'side': side,  
            'type': 'MARKET',  
        } 
        responce = self.orders_request(**params)  
        return responce  

    def get_open_orders(self):  
        open_orders = []   
        if self.market == 'spot':
            try:
                open_orders = self.binance_python_client.get_open_orders()                
            except Exception as ex:
                print(ex)
        elif self.market == 'futures':
            try:
                open_orders = self.binance_python_client.futures_get_open_orders()                
            except Exception as ex:
                print(ex)

        return open_orders

    def cancel_all_orderss(self):
        open_orders = []
       
        for _ in range(3):
            if self.market == 'spot':
                open_orders = self.get_open_orders()
                print(f"Open orders before canceling: {len(open_orders)}")
                for order in open_orders:
                    try:
                        self.binance_python_client.cancel_order(symbol=order['symbol'], orderId=order['orderId'])
                    except Exception as ex:
                        print(ex)
                open_orders = self.get_open_orders()
                print(f"Open orders after canceling: {len(open_orders)}")

                if len(open_orders) == 0:
                    break

            elif self.market == 'futures':
                open_orders = self.get_open_orders()
                print(f"Open orders before canceling: {len(open_orders)}")                
                try:
                    self.binance_python_client.futures_cancel_all_open_orders()
                except Exception as ex:
                    print(ex)
                open_orders = self.get_open_orders()
                print(f"Open orders after canceling: {len(open_orders)}")

                if len(open_orders) == 0:
                    break        
    
create_orders_obj = CREATE_BINANCE_ORDER(market='spot', test_flag=False)


        