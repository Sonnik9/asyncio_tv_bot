# import websocket
# import threading
# import json
# import time

# class SocketConn(websocket.WebSocketApp):
    
#     def __init__(self, url):
#         super().__init__(url=url, on_open=self.on_open)
#         self.on_message = lambda ws, msg: self.message(msg)
#         self.on_error = lambda ws, e: print("Error", e)
#         self.on_close = lambda ws: print("Closing")

        

#     def on_open(self, ws):
#         print("Websocket was opened")

#     def message(self, msg):
#         if not msg:
#            self.run_forever()
#         time.sleep(1)
#         data = json.loads(msg)
#         answer = f"{data['s']}:  {data['k']['c']}"
#         # print(answer)
#         return answer

# def main():
#     max_threads = 1
#     socket_kline_time, socket_time_frame = '1', 'h'
#     # interval = 
#     socket_main_url_pattern = 'wss://stream.binance.com:9443/ws/'
#     top_coins = ['BTCUSDT']
#     # ['CELOUSDT', 'SUSHIUSDT', 'YFIUSDT', 'MASKUSDT', 'LINKUSDT', 'JASMYUSDT', 'KSMUSDT', 'AGLDUSDT', 'BNXUSDT', 'XTZUSDT', 'EOSUSDT', '1000PEPEUSDT', 'MANAUSDT', 'STXUSDT', 'LPTUSDT', 'CRVUSDT', 'OGNUSDT', 'QTUMUSDT', 'FLOWUSDT', 'HOTUSDT'] 
                 
#     # if len(top_coins) > max_threads:
#     #     top_coins = top_coins[:max_threads]

#     # for item in top_coins:
#     urll = f"{socket_main_url_pattern}{top_coins[0].lower()}@kline_{socket_kline_time}{socket_time_frame}"
#     # urll = f"{socket_main_url_pattern}{top_coins[0].lower()}@kline_1m"
#     print(urll)
#     # continue
#     # threading.Thread(target=SocketConn, args=(urll,)).start()
#     # msg = None
#     # answer = None
#     # sok = SocketConn(urll)
#     # answer = sok.message(msg)
#     # print(f"49str:___{answer}")
#         # break

# if __name__=="__main__":
#     main()

# # killall -9 python

# # {"e":"kline","E":1694257342001,"s":"BTCUSDT","k":{"t":1694257341000,"T":1694257341999,"s":"BTCUSDT","i":"1s","f":3208445435,"L":3208445440,"o":"25869.25000000","c":"25869.25000000","h":"25869.26000000","l":"25869.25000000","v":"0.02848000","n":6,"x":true,"q":"736.75639920","V":"0.01592000","Q":"411.83861920","B":"0"}}


# ['XVGUSDT', 'CHRUSDT', 'STORJUSDT', 'WAVESUSDT', 'UMAUSDT', 'BNXUSDT', 'SXPUSDT', 'XLMUSDT', 'DARUSDT', 'PENDLEUSDT', 'TRUUSDT', 'IOTXUSDT', 'ACHUSDT', 'CELRUSDT', 'CTSIUSDT', 'CELOUSDT', 'AUDIOUSDT', 'ONEUSDT', 'CKBUSDT', 'TUSDT']



    # streams_url = 'wss://stream.binance.com:9443/stream?streams='
    # awerage_socket_url = 'wss://stream.binance.com:9443/ws/'
    
    # url = awerage_socket_url
    # socket_kline_time, socket_time_frame = 1, 'm'
    # top_coins = ['BTCUSDT', 'ETHUSDT'] 

    # stream = [f"{x.lower()}@kline_{socket_kline_time}{socket_time_frame}" for x in top_coins]
    # print(stream)

# import asyncio
# import time
# from API.bin_data_get import bin_data
# from pparamss import my_params
# from ENGIN.tv_signals_1 import get_orders_stek
# from MONEY.stop_logic_1 import tp_sl_strategy_1_func
# from UTILS.waiting_candle import kline_waiter

# current_stake_list = set()

# async def stops_monitor(symbol, defender):
#     url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1s'
    
#     close_position = False
#     qnt = 0.001
#     first_price_flag = False
#     enter_price = None
    
#     async with websockets.connect(url) as websocket:
#         try:
#             async for message in websocket:
#                 data = json.loads(message)
#                 print(f"{data['s']}:  {data['k']['c']}")
#                 if not first_price_flag:
#                     enter_price = float(data['k']['c'])
#                     first_price_flag = True
#                     continue
#                 else:
#                     current_price = float(data['k']['c'])
#                     profit, close_position = tp_sl_strategy_1_func(enter_price, current_price, qnt, defender)

#                     await asyncio.sleep(5)

#                 if close_position:
#                     return profit
#         except Exception as e:
#             print(f"An error occurred: {e}")


# async def threads_controller(symbol, defender):
#     profit = None
#     if symbol:
#         current_stake_list.add(symbol)
#         profit = await stops_monitor(symbol, defender)
    
#     if profit:
#         current_stake_list.remove(symbol)

# async def setup_tasks(first_order_stake):
#     tasks = []
    
#     for symbol, defender in first_order_stake:
#         if symbol not in current_stake_list:
#             current_stake_list.add(symbol)
#             task = asyncio.create_task(threads_controller(symbol, defender))
#             tasks.append(task)
    
#     await asyncio.gather(*tasks)

# async def main():
#     top_coins = None
    
#     try:
#         top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins)
#     except Exception as ex:
#         print(f"main__54:\n{ex}")
    
#     # print(top_coins)
    
#     try:
#         wait_time = kline_waiter(my_params.kline_time, my_params.time_frame)
#         print(f"waiting time to close last candle is: {wait_time} sec")
#     except Exception as ex:
#         print(f"main__63:\n{ex}")
    
#     while True:
#         try:
#             first_stake = []
#             first_added_stake = []
#             first_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)
            
#             if first_stake:
#                 first_stake = first_stake[:2]
                
#                 if len(first_stake) > my_params.max_threads:
#                     first_stake = first_stake[:my_params.max_threads]
                
#                 if len(first_stake) < my_params.max_threads:
#                     for _ in range(my_params.max_threads - len(first_stake)):
#                         first_added_stake.append((None, None))
#                     first_stake += first_added_stake
                
#                 await setup_tasks(first_stake)
#                 break
#             else:
#                 await asyncio.sleep(5)
#         except Exception as ex:
#             print(f"main__69:\n{ex}")
    
#     print("The first_stake was launched successfully!")

# if __name__ == "__main__":
#     import websockets
#     import json
#     asyncio.run(main())
