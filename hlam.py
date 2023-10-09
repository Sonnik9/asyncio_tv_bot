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

# import asyncio
# import time
# from API.bin_data_get import bin_data
# from pparamss import my_params
# from ENGIN.tv_signals_1 import get_orders_stek
# from UTILS.waiting_candle import kline_waiter
# from taskss import setup_tasks
# import time
# import asyncio 
# from asynccc import shell_monitiringg
# from ENGIN.tv_signals_1 import get_orders_stek
# from pparamss import my_params
# from API.bin_data_get import bin_data
# import pytz
# from datetime import datetime, time
# stake_list_lock = asyncio.Lock()
# current_stake_list = set()
# profit_variable_lock = asyncio.Lock()
# profit_list = []
# # counter_variable_lock = asyncio.Lock()
# # counter_var = 0

# import websockets
# import asyncio
# import json
# from MONEY.stop_logic_1 import tp_sl_strategy_1_func

# async def price_monitoring(symbol, defender):
#     url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1s'
#     profit = None
#     close_position = False
#     qnt = 0.001
#     first_price_flag = False

#     while True:
#         try:
#             async with websockets.connect(url) as websocket:
#                 async for message in websocket:
#                     data = json.loads(message)
#                     # print(f"{data['s']}:  {data['k']['c']}")
#                     if not first_price_flag:
#                         enter_price = float(data['k']['c'])
#                         first_price_flag = True
#                         continue
#                     else:
#                         current_price = float(data['k']['c'])
#                         profit, close_position = tp_sl_strategy_1_func(enter_price, current_price, qnt, defender)

#                         await asyncio.sleep(5)

#                     if close_position:
#                         return profit, symbol
                    
#         except websockets.exceptions.ConnectionClosed:
#             print("Connection closed unexpectedly. Reconnecting...")
#             await asyncio.sleep(7)  # Подождать перед повторной попыткой подключения
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             await asyncio.sleep(7)
#         finally:
#             await websocket.close()
#             break

#     return profit, symbol

# async def shell_monitiringg(symbol, defender):
#     profit = None
#     profit, symbol = await price_monitoring(symbol, defender)
    
#     return profit, symbol




# def asum_counter(profitt):
#     win_rate = sum([1 for x in profitt if x >0])
#     lose_rate = sum([1 for x in profitt if x <0])
#     total = sum(profitt)
#     win_per = (win_rate * 100)/(win_rate + lose_rate)
#     result = f"total: {total}$ \n win_per: {win_per}%"
#     with open('result.txt', 'w') as txt_file:
#         txt_file.write(result) 


# async def tasks_controller(symbol, defender):
#     profit = None
#     next_stake = None
#     symbol_to_remove = None

#     while True:
#         await asyncio.sleep(2)
#         now = datetime.now()
#         desired_timezone = pytz.timezone('Europe/Kiev')
#         now_in_desired_timezone = now.astimezone(desired_timezone)
#         current_time = now_in_desired_timezone.strftime('%H:%M')
#         # print(current_time)

#         if time(21, 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(23, 0):
#             print('it is time for rest!')
#             async with profit_variable_lock:
#                 asum_counter(profit_list)
#                 break

#         if symbol:
#             try:
#                 async with stake_list_lock:
#                     current_stake_list.add(symbol)
#                 profit, symbol_to_remove = await shell_monitiringg(symbol, defender)
#                 if profit:
#                     async with profit_variable_lock:
#                         profit_list.append(profit)
#                         if len(profit_list) >= 10:
#                             asum_counter(profit_list)
#                             break

#                 print(f"tasks_19:___{profit}")
#                 symbol = None
#                 async with stake_list_lock:
#                     try:
#                         current_stake_list.remove(symbol_to_remove)
#                         print(f"after_removing:___{current_stake_list}")                        
#                     except Exception as ex:
#                         print(ex)
#             except Exception as ex:
#                 print(ex)

#         else:
#             try:
#                 top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins) 
#                 next_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)
#             except Exception as ex:
#                 print(ex)
#             if next_stake:
#                 async with stake_list_lock: 
#                     for symboll, defenderr in next_stake:                        
#                         if (len(current_stake_list) < my_params.max_threads) and symboll not in current_stake_list:                                        
#                             current_stake_list.add(symboll)
#                             print(f"after_adding:___{current_stake_list}")
#                             symbol, defender = symboll, defenderr                     
#                             break
#             else:
#                 await asyncio.sleep(12)

# async def setup_tasks(initial_stake):
#     tasks = []
   
#     for symbol, defender in initial_stake:
#         task = asyncio.create_task(tasks_controller(symbol, defender))
#         tasks.append(task)
    
#     await asyncio.gather(*tasks)


# # python -m taskss

# async def main():
#     # sys.exit()
#     # loop = asyncio.get_event_loop()
#     # loop.close()
#     top_coins = None
    
#     try:
#         top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins)
#     except Exception as ex:
#         print(f"main__15:\n{ex}")
    
#     # print(top_coins)
    
#     try:
#         wait_time = kline_waiter(my_params.kline_time, my_params.time_frame)
#         print(f"waiting time to close last candle is: {wait_time} sec")
#         # await asyncio.sleep(wait_time)
#     except Exception as ex:
#         print(f"main__24:\n{ex}")
    
#     while True:
#         try:
#             first_stake = []
#             first_added_stake = []
#             first_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)            
#             if first_stake:
#                 break
#             else:
#                 await asyncio.sleep(5)
#         except Exception as ex:
#             print(f"main__39:\n{ex}")
#     try:
#         # first_stake = first_stake[:2]
        
#         if len(first_stake) > my_params.max_threads:
#             first_stake = first_stake[:my_params.max_threads]
        
#         if len(first_stake) < my_params.max_threads:
#             for _ in range(my_params.max_threads - len(first_stake)):
#                 first_added_stake.append((None, None))
#             first_stake += first_added_stake
#         print(first_stake)
#         await setup_tasks(first_stake)
#     except Exception as ex:
#         print(f"main__51:\n{ex}")
    
    
#     print("The first_stake was launched successfully!")

# if __name__ == "__main__":
#     asyncio.run(main())


    # streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']

            # except aiohttp.ClientError as e:
            #     print(f"An error occurred: {e}")
            #     await asyncio.sleep(7) 
            #     continue 
            # except ws.exceptions.ConnectionClosed:
            #     print(f"An error occurred:...")
            #     await asyncio.sleep(7)  
            #     continue



# async def price_monitoring(main_stake):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     profit = None
#     close_position = False
#     qnt = 0.001
#     first_price_flag = False
#     websocket = None
#     # streams = [f'{item[0].lower()}@kline_1s' for item in main_stake]
#     # print(streams)
#     streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
#     # return
#     try:
#         while True:
#             try:
#                 print('hi')
#                 async with websockets.connect(url) as websocket:
#                     subscribe_request = {
#                         "method": "SUBSCRIBE",
#                         "params": streams,
#                         "id": 87
#                     }

#                     await websocket.send(json.dumps(subscribe_request))
#                     await websocket.recv()
                    
#                     async for message in websocket:
#                         data = json.loads(message)
#                         print(data)
#                         break 
#                     break
#                         # await asyncio.sleep(5)
#                         # return
#                         # print(f"{data['s']}:  {data['k']['c']}")
#                         # if not first_price_flag:
#                         #     enter_price = float(data['k']['c'])
#                         #     first_price_flag = True
#                         #     continue
#                         # else:
#                         #     current_price = float(data['k']['c'])
#                         #     profit, close_position = tp_sl_strategy_1_func(enter_price, current_price, qnt, defender)

#                         #     await asyncio.sleep(5)

#                         # if close_position:
#                             # return profit, symbol
                        
#             except websockets.exceptions.ConnectionClosed:
#                 print("Connection closed unexpectedly. Reconnecting...")
#                 await asyncio.sleep(7)  # Подождать перед повторной попыткой подключения
#                 continue
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 await asyncio.sleep(7)
#                 continue
#     except:
#         pass
#     finally:
#         await websocket.close()
        

    # return profit, symbol



# async def tasks_maneger(initial_stake):
#     symbol, defender = initial_stake[0], initial_stake[1]
#     profit = None
#     next_stake = None
#     symbol_to_remove = None

#     while True:
#         await asyncio.sleep(2)
#         now = datetime.now()
#         desired_timezone = pytz.timezone('Europe/Kiev')
#         now_in_desired_timezone = now.astimezone(desired_timezone)
#         current_time = now_in_desired_timezone.strftime('%H:%M')
#         # print(current_time)

#         if time(21, 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(23, 0):
#             print('it is time for rest!')
#             async with profit_variable_lock:
#                 asum_counter(profit_list)
#                 break

#         if symbol:
#             try:
#                 async with stake_list_lock:
#                     current_stake_list.add(symbol)
#                 profit, symbol_to_remove = await shell_monitiringg(symbol, defender)
#                 if profit:
#                     async with profit_variable_lock:
#                         profit_list.append(profit)
#                         if len(profit_list) >= 10:
#                             asum_counter(profit_list)
#                             break

#                 print(f"tasks_19:___{profit}")
#                 symbol = None
#                 async with stake_list_lock:
#                     try:
#                         current_stake_list.remove(symbol_to_remove)
#                         print(f"after_removing:___{current_stake_list}")                        
#                     except Exception as ex:
#                         print(ex)
#             except Exception as ex:
#                 print(ex)

#         else:
#             try:
#                 top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins) 
#                 next_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)
#             except Exception as ex:
#                 print(ex)
#             if next_stake:
#                 async with stake_list_lock: 
#                     for symboll, defenderr in next_stake:                        
#                         if (len(current_stake_list) < my_params.max_threads) and symboll not in current_stake_list:                                        
#                             current_stake_list.add(symboll)
#                             print(f"after_adding:___{current_stake_list}")
#                             symbol, defender = symboll, defenderr                     
#                             break
#             else:
#                 await asyncio.sleep(12)


            # return


            
            # if len(first_stake) < my_params.max_threads:
            #     for _ in range(my_params.max_threads - len(first_stake)):
            #         first_added_stake.append((None, None))
            #     first_stake += first_added_stake
            # print(first_stake)

    # loop = asyncio.get_event_loop()
    # loop.close()

            # # await asyncio.sleep(2)
            # now = datetime.now()
            # desired_timezone = pytz.timezone('Europe/Kiev')
            # now_in_desired_timezone = now.astimezone(desired_timezone)
            # current_time = now_in_desired_timezone.strftime('%H:%M')
            # # print(current_time)
            # if time(21, 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(23, 0):
            #     print('it is time to assuming!')
            #     async with profit_variable_lock:
            #         asum_counter(raport_list)
            #         break

# import asyncio
# import json
# import websockets
# from asyncio import Queue

# async def price_monitoring(main_stake, data_queue):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     websocket = None
#     streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
    
#     try:
#         while True:
#             try:
#                 async with websockets.connect(url) as websocket:
#                     subscribe_request = {
#                         "method": "SUBSCRIBE",
#                         "params": streams,
#                         "id": 87
#                     }

#                     await websocket.send(json.dumps(subscribe_request))
                    
#                     async for message in websocket:
#                         data = json.loads(message)
#                         await data_queue.put(data)

#             except websockets.exceptions.ConnectionClosed:
#                 print("Connection closed unexpectedly. Reconnecting...")
#                 await asyncio.sleep(7)
#                 continue
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 await asyncio.sleep(7)
#                 continue
#     except KeyboardInterrupt:
#         pass
#     finally:
#         if websocket:
#             await websocket.close()

# async def process_data(data_queue):
#     while True:
#         data = await data_queue.get()
#         # Вместо этой строки добавьте вашу логику обработки данных из стрима
#         print("Received data:", data)

# if __name__ == "__main__":
#     main_stake = []  # Здесь добавьте свой список символов для мониторинга
#     data_queue = asyncio.Queue()

#     loop = asyncio.get_event_loop()
#     loop.create_task(price_monitoring(main_stake, data_queue))
#     loop.create_task(process_data(data_queue))
    
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         loop.run_until_complete(asyncio.gather(*asyncio.all_tasks()))
#         loop.close()


# import asyncio
# import json
# import websockets

# async def price_monitoring(main_stake, data_callback):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     websocket = None
#     streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
#     data_buffer = {}  # Здесь будем хранить данные для каждого стрима

#     try:
#         async with websockets.connect(url) as websocket:
#             subscribe_request = {
#                 "method": "SUBSCRIBE",
#                 "params": streams,
#                 "id": 87
#             }
#             await websocket.send(json.dumps(subscribe_request))

#             async for message in websocket:
#                 data = json.loads(message)
#                 symbol = data['s']

#                 if symbol not in data_buffer:
#                     data_buffer[symbol] = []

#                 data_buffer[symbol].append(data)

#                 # Проверяем, есть ли достаточно данных для каждого стрима
#                 if all(len(data_buffer[s]) > 0 for s in streams):
#                     # Вызываем обратную функцию с собранными данными
#                     await data_callback(data_buffer)
#                     # Очищаем буфер
#                     data_buffer = {s: [] for s in streams}

#     except websockets.exceptions.ConnectionClosed:
#         print("Connection closed unexpectedly. Reconnecting...")
#         await asyncio.sleep(7)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         await asyncio.sleep(7)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         if websocket:
#             await websocket.close()

# async def process_data(data_buffer):
#     # Обрабатываем данные из буфера
#     for symbol, data_list in data_buffer.items():
#         print(f"Received data for {symbol}: {data_list}")
#         # Вместо этой строки добавьте вашу логику обработки данных из стримов

# if __name__ == "__main__":
#     main_stake = []  # Здесь добавьте свой список символов для мониторинга

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(price_monitoring(main_stake, process_data))


# import json
# import websockets
# import asyncio

# async def price_monitoring(main_stake, data_callback):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
    
#     try:
#         async with websockets.connect(url) as websocket:
#             subscribe_request = {
#                 "method": "SUBSCRIBE",
#                 "params": streams,
#                 "id": 87
#             }
#             await websocket.send(json.dumps(subscribe_request))
#             await websocket.recv()
            
#             data_list = []
#             async for message in websocket:
#                 data = json.loads(message)
#                 data_list.append(data)
                
#                 if len(data_list) == len(streams):
#                     await data_callback(data_list)
#                     data_list = []

#     except websockets.exceptions.ConnectionClosed:
#         print("Connection closed unexpectedly. Reconnecting...")
#         await asyncio.sleep(7)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         await asyncio.sleep(7)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         await websocket.close()

# # Функция для обработки данных
# async def process_data(data_list):
#     # for data in data_list:
#     print(data_list)
#         # Вместо этой строки добавьте вашу логику обработки данных из стрима

# if __name__ == "__main__":
#     main_stake = []  # Здесь добавьте свой список символов для мониторинга

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(price_monitoring(main_stake, process_data))

# import aiohttp
# import asyncio
# import json

# async def price_monitoring(main_stake, data_callback):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']

#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.ws_connect(url) as ws:
#                 subscribe_request = {
#                     "method": "SUBSCRIBE",
#                     "params": streams,
#                     "id": 87
#                 }
#                 await ws.send_json(subscribe_request)

#                 data_list = []
#                 async for msg in ws:
#                     if msg.type == aiohttp.WSMsgType.TEXT:
#                         data = json.loads(msg.data)
#                         data_list.append(data)

#                         if len(data_list) >= len(streams):
#                             await data_callback(data_list)
#                             data_list = []

#     except aiohttp.ClientError as e:
#         print(f"An error occurred: {e}")

# # Функция для обработки данных
# async def process_data(data_list):
#     data_list = json.load(data_list)
#     new_list = []
#     for data in data_list:
#         new_list.append((data['data']['s'], data['data']['k']['c']))
#     print(new_list)
#         # Вместо этой строки добавьте вашу логику обработки данных из стрима

# if __name__ == "__main__":
#     main_stake = []  # Здесь добавьте свой список символов для мониторинга

#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(price_monitoring(main_stake, process_data))
#     asyncio.run(price_monitoring(main_stake, process_data))

# import aiohttp
# import asyncio
# import json

# async def price_monitoring(main_stake, data_callback):
#     url = f'wss://stream.binance.com:9443/stream?streams='
#     profit = None
#     close_position = False
#     qnt = 0.001
#     first_price_flag = False
#     ws = None
#     streams = [f'{item[0].lower()}@kline_1s' for item in main_stake]
#     # streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
#     try:
#         while True:                
#             try:
#                 print('hi')
#                 async with aiohttp.ClientSession() as session:
#                     async with session.ws_connect(url) as ws:
#                         subscribe_request = {
#                             "method": "SUBSCRIBE",
#                             "params": streams,
#                             "id": 87
#                         }
#                         await ws.send_json(subscribe_request)

#                         data_list = []
#                         async for msg in ws:
#                             if msg.type == aiohttp.WSMsgType.TEXT:
#                                 try:
#                                     data = json.loads(msg.data)                            
#                                     symbol = data.get('data',{}).get('s')
#                                     close_price = float(data.get('data',{}).get('k',{}).get('c'))
#                                     data_list.append((symbol, close_price))
#                                 except:
#                                     pass

#                                 if len(data_list) == len(streams):
#                                     await data_callback(data_list, main_stake)
#                                     data_list = []

#             except aiohttp.ClientError as e:
#                 print(f"An error occurred: {e}")
#                 await asyncio.sleep(7)  
#                 continue
#             except ws.exceptions.ConnectionClosed:
#                 await asyncio.sleep(7)  
#                 continue
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 await asyncio.sleep(7)
#                 continue
#     except:
#         pass
#     finally:
#         await ws.close()

# async def process_data(data_list, main_stake):
#     # print(data_list)
#     # print('/'*20)
#     formated_price_list = []
#     for symbol, close_price in data_list:
#         for s, d in main_stake:
#             if symbol==s:
#                 formated_price_list.append(symbol, d, close_price)
#                 break
    
#     print(formated_price_list)
#     print('/'*100)


# import os
# import psutil

# num_cores = os.cpu_count()
# print(f"Количество ядер процессора: {num_cores}")


# # Загруженность процессора в процентах
# cpu_usage = psutil.cpu_percent(interval=1)
# print(f"Загруженность процессора: {cpu_usage}%")

# # python cpu_test.py

# async def process_data(intermedeate_data_list, enter_price_list, main_stake):
#     print(len(enter_price_list))
#     print(len(main_stake))
#     profit_flag = False

#     for symbol, current_price in intermedeate_data_list:  
#         for item in main_stake:
#             if symbol==item['symbol']:
#                 item['current_price'] = current_price
#                 break
#     for symboll, enter_pr in enter_price_list:
#         for item2 in main_stake:
#             if (symboll == item2['symbol']) and not item2['in_position']:
#                 item2['enter_price'] = enter_pr
#                 break
#             elif (symboll == item2['symbol']) and item2['in_position']:
#                 item2['enter_price'] = item2['enter_price']
#                 break
#     try:         
#         main_stake, profit_flag = sl_tp_logic(main_stake)
#     except Exception as ex:
#         print(ex)
    
#     # print(new_formated_data)
#     # print(formated_data)
#     # print('/'*100)
#     return main_stake, profit_flag

# async def process_data(intermediate_data_list, enter_price_list, main_stake):
#     print(f"process_data_enter_price_list:__{len(enter_price_list)}")
#     print(f"process_data_intermediate_data_list:__{len(enter_price_list)}")
#     print(f"process_data_main_stake_before:__{len(main_stake)}")

#     symbol_to_item = {item['symbol']: item for item in main_stake}
    
#     profit_flag = False
#     symbol_count = len(symbol_to_item)

#     print(f"symbol_to_item before: {symbol_count}")


#     for symbol, current_price in intermediate_data_list:
#         if symbol in symbol_to_item:
#             symbol_to_item[symbol]['current_price'] = current_price
#         # else:
#         #     print('Problem 1')
#     symbol_count = len(symbol_to_item)
#     print(f"symbol_to_item after 1: {symbol_count}")

#     for symbol, enter_price in enter_price_list:
#         if symbol in symbol_to_item and not symbol_to_item[symbol]['in_position']:
#             symbol_to_item[symbol]['enter_price'] = enter_price
#         # elif symbol in symbol_to_item and symbol_to_item[symbol]['in_position']:
#         #     symbol_to_item[symbol]['enter_price'] = symbol_to_item[symbol]['enter_price']
#         #     print(symbol_to_item[symbol]['enter_price'])
#         # if symbol not in symbol_to_item:
#         #     print('Problem 2')
#     symbol_count = len(symbol_to_item)

#     main_stake = list(symbol_to_item.values())
#     print(f"process_data_main_stake_after_1:__{len(main_stake)}")

#     try:
#         main_stake, profit_flag = sl_tp_logic(main_stake)
#     except Exception as ex:
#         print(f"125:__{ex}")
#     print(f"process_data_main_stake_after_2:__{len(main_stake)}")

#     return main_stake, profit_flag



# def sl_tp_logic(main_stake):
#     depo = 200 # 20*10    
#     sl_q = 0.00001
#     tp_q = 0.000015
#     profit_flag = False

#     for item1 in main_stake:
#         if not item1['in_position']:
#             # open_order func
#             item1['in_position'] = True
    
#     for item in main_stake:
#         profit = None
#         # profit, symbol, defender, enter_price, current_price, in_position, close_order
#         if item['enter_price']:
#             try:
#                 qnt = round((depo/item['enter_price']), 7)
#             except Exception as ex:
#                 print(f"MONEY/stop_logic_1.py_str22:___{ex}")

#         try:
#             if item['defender'] == 1:

#                 if item['current_price'] >= item['enter_price'] + (item['enter_price']*tp_q):   
#                     profit = (item['current_price'] - item['enter_price'])*qnt
#                     # close_order func
#                     item['close_order'] = True   
#                     item['profit'] = profit
#                     profit_flag = True

        
#                 elif item['current_price'] <= item['enter_price'] - (item['enter_price']*sl_q):            
#                     profit = (item['current_price'] - item['enter_price'])*qnt
#                     # close_order func
#                     item['close_order'] = True   
#                     item['profit'] = profit   
#                     profit_flag = True   
        
#             elif item['defender'] == -1:            
#                 if item['current_price'] <= item['enter_price'] - (item['enter_price']*tp_q):               
#                     profit = (item['enter_price'] - item['current_price'])*qnt
#                     # close_order func
#                     item['close_order'] = True  
#                     item['profit'] = profit 
#                     profit_flag = True
        
#                 elif item['current_price'] >= item['enter_price'] + (item['enter_price']*sl_q):                
#                     profit = (item['enter_price'] - item['current_price'])*qnt  
#                     # close_order func
#                     item['close_order'] = True  
#                     item['profit'] = profit
#                     profit_flag = True
#         except Exception as ex:
#             print(f"MONEY/stop_logic_1.py_str55:___{ex}")

#     return main_stake, profit_flag


    # def get_klines(self,):
    #     # /api/v3/klines
    #     symbols = []
    #     klines = None
    #     method = 'GET'
    #     params = {}

# from tradingview_ta import TA_Handler, Interval, Exchange


# from UTILS import indicators
# from API.bin_data_get import bin_data
# from pparamss import my_params

# class IND_STR_TWO():

#     def __init__(self) -> None:
#         pass

#     def bunch_handler_func(self, next_data, close_price, current_bunch):
#         b_bband_q, s_bband_q, b_rsi_lev, s_rsi_lev, b_macd__q, s_macd_q, b_stoch_q, s_stoch_q = 1, 1, 33, 67, 1, 1, 23, 77

#         signals_sum = []
#         buy_signals_counter = 0
#         sell_signals_counter = 0
#         buy_total_signal, sell_total_signal = False, False

#         if 'bband_flag' in current_bunch:
#             upper, lower = indicators.calculate_bollinger_bands(next_data)        
#             buy_bband_signal = close_price >= lower * b_bband_q
#             sell_bband_signal = close_price <= upper * s_bband_q
#             signals_sum.append((buy_bband_signal, sell_bband_signal))

#         if 'macd_strong_flag' in current_bunch:
#             macd, signal = indicators.calculate_macd(next_data)        
#             buy_strong_macd_signal = (macd > signal * b_macd__q) & (macd < 0)
#             sell_strong_macd_signal = (macd < signal * s_macd_q) & (macd > 0)
#             signals_sum.append((buy_strong_macd_signal, sell_strong_macd_signal))

#         if 'macd_lite_flag' in current_bunch:
#             macd, signal = indicators.calculate_macd(next_data)        
#             buy_lite_macd_signal = macd > signal * b_macd__q
#             sell_lite_macd_signal = macd < signal * s_macd_q
#             signals_sum.append((buy_lite_macd_signal, sell_lite_macd_signal))

#         if 'rsi_flag' in current_bunch:
#             rsi = indicators.calculate_rsi(next_data)        
#             buy_rsi_signal = rsi <= b_rsi_lev
#             sell_rsi_signal = rsi >= s_rsi_lev
#             signals_sum.append((buy_rsi_signal, sell_rsi_signal))

#         if 'stoch_flag' in current_bunch:
#             fastk, slowk = indicators.calculate_stochastic_oscillator(next_data)        
#             buy_stoch_signal = (fastk > slowk) & (fastk < b_stoch_q)
#             sell_stoch_signal = (fastk < slowk) & (fastk > s_stoch_q)
#             signals_sum.append((buy_stoch_signal, sell_stoch_signal))

#         if 'engulfing_flag' in current_bunch:
#             engulfing = indicators.calculate_engulfing_patterns(next_data)
            
#             buy_engulfing_signal = engulfing > 0
#             sell_engulfing_signal = engulfing < 0
#             signals_sum.append((buy_engulfing_signal, sell_engulfing_signal))

#         if 'doji_flag' in current_bunch:
#             doji = indicators.calculate_doji(next_data)
            
#             buy_doji_signal = doji != 0
#             sell_doji_signal = doji != 0
#             signals_sum.append((buy_doji_signal, sell_doji_signal))

#         for buy_signal, sell_signal in signals_sum:
#             if buy_signal:
#                 buy_signals_counter += 1
#             if sell_signal:
#                 sell_signals_counter += 1

#         if 'U' in current_bunch:
#             if buy_signals_counter == len(signals_sum):
#                 buy_total_signal = True 
#         if 'D':
#             if sell_signals_counter == len(signals_sum):
#                 sell_total_signal = True
#         if 'F' in current_bunch:
#             if buy_signals_counter == len(signals_sum):
#                 buy_total_signal = True 
#             if sell_signals_counter == len(signals_sum):
#                 sell_total_signal = True

#         return buy_total_signal, sell_total_signal

#     def trends_defender(self, next_data, close_price):
#         try:
#             adx = indicators.calculate_adx(next_data)        
#             sma = indicators.calculate_sma(next_data)        
#         except Exception as ex:
#             print(ex)
#         if close_price > sma and adx > 25:
#             return "U"

#         elif close_price < sma and adx > 25:
#             return "D"
#         else:
#             return "F"

#     def signal_gen(self, coin): 
#         try:
#             klines = bin_data.get_klines(coin)
            
#             next_data, close_price = klines, klines["Close"].iloc[-1]
#             # print(close_price)
#         except:
#             return "neutral"
#         bunch_variant = 2   
        
#         buy_signal, sell_signal = False, False
#         trende_sign = self.trends_defender(next_data, close_price)
                    
#         if trende_sign == 'U':
#             current_bunch = ['bband_flag', 'macd_lite_flag', 'engulfing_flag', 'U']
#         if trende_sign == 'D':
#             current_bunch = ['bband_flag', 'macd_lite_flag', 'engulfing_flag', 'D']
            
#         if trende_sign == 'F':
#             if bunch_variant == 2:
#                 current_bunch = ['macd_lite_flag', 'stoch_flag', 'F']

#         buy_signal, sell_signal = self.bunch_handler_func(next_data, close_price, current_bunch)

#         if buy_signal:
#             return 1
#         elif sell_signal:
#             return 2
#         else:
#             return "neutral"
            
#     def get_udf_strategy_signals(self, top_coins):
#         usual_defender_stake = []
#         for coin in top_coins:
#             defender = self.signal_gen(coin)
#             print(defender)
#             if defender != "neutral":
#                 # print(defender)
#                 usual_defender_stake.append((coin, defender))
#             if len(usual_defender_stake) == my_params.max_threads:
#                 break 

#         return usual_defender_stake



       

# get_orders_stek_2 = IND_STR_TWO()





# import talib

# def calculate_adx(data, period=14):
#     adx = None
#     try:
#         adx = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=period)
#         adx = adx.to_numpy()[-1]
#     except Exception as ex:
#         print(f"34 indicatorss:___{ex}")
#     return adx

# def calculate_sma(data, period=20):
#     sma = None
#     num_std = 2
#     try:
#         _, sma, _ = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std)
#         sma = sma.to_numpy()[-1]
#     except Exception as ex:
#         print(ex)
#     return sma

# def calculate_bollinger_bands(data, period=20, num_std=2):
#     upper_band, _, lower_band = None, None, None
#     try:
#         upper_band, _, lower_band = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std)
#         upper_band = upper_band.to_numpy()[-1]
#         lower_band = lower_band.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_bollinger_bands: {ex}")
#     return upper_band, lower_band

# def calculate_rsi(data, period=14):
#     rsi = None
#     try:
#         rsi = talib.RSI(data['Close'], timeperiod=period)
#         rsi.interpolate(method='linear', inplace=True)
#         rsi = rsi.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_rsi: {ex}")
#     return rsi

# def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
#     macd, signal = None, None
#     try:
#         macd, signal, _ = talib.MACD(data['Close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
#         macd = macd.to_numpy()[-1]
#         signal = signal.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_macd: {ex}")
#     return macd, signal

# # def calculate_atr(data, period=14):
# #     atr = None
# #     try:
# #         atr = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=period)
# #         atr = atr.to_numpy()[-1]
# #         # atr = atr[-1]
# #     except Exception as ex:
# #         print(f"Error in calculate_atr: {ex}")
# #     return atr

# def calculate_engulfing_patterns(data):
#     engulfing = None
#     try:
#         engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
#         engulfing = engulfing.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_engulfing_patterns: {ex}")
#     return engulfing

# def calculate_doji(data):
#     doji = None
#     try:
#         doji = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
#         doji = doji.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_doji: {ex}")
#     return doji

# def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
#     slow_k, slow_d = None, None
#     try:
#         slow_k, slow_d = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=k_period, slowk_period=k_period, slowd_period=d_period)
#         slow_k = slow_k.to_numpy()[-1]
#         slow_d = slow_d.to_numpy()[-1]
#     except Exception as ex:
#         print(f"Error in calculate_stochastic_oscillator: {ex}")
#     return slow_k, slow_d


# def calculate_atr(data, period=14):
#     true_ranges = []

#     for i in range(1, len(data)):
#         high = data['High'].iloc[i]
#         low = data['Low'].iloc[i]
#         close = data['Close'].iloc[i - 1]

#         true_range = max(high - low, abs(high - close), abs(low - close))
#         true_ranges.append(true_range)

#     atr = sum(true_ranges[:period]) / period
#     # print(atr)

#     # for i in range(period, len(data)):
#     #     atr = ((atr * (period - 1)) + true_ranges[i]) / period
#     # print(atr)

#     return atr

    
    # def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt):
    #         profit = None
    #         self.s_l = 0.04
    #         # print(defender, enter_price, current_price, atr, qnt)

    #         if defender == 1: 
    #             self.checkpoint = enter_price*(1 + self.counter/100)
    #             self.tralling_s_l = enter_price + ((self.checkpoint - enter_price)/2)
    #             if current_price > enter_price:
    #                 if current_price >= self.checkpoint:
    #                     self.tralling_flag = True
    #                     self.counter += 1
    #                     if self.counter == 2:
    #                         self.counter = 0
    #                         # print('realy i am here')
    #                         self.tralling_flag = False
    #                         profit = (current_price - enter_price)*qnt
    #                         return True, profit                   
    #                 if (current_price <= self.tralling_s_l) and self.tralling_flag:
    #                     self.counter = 0
    #                     # print('hi2')
    #                     self.tralling_flag = False
    #                     profit = (current_price - enter_price)*qnt
    #                     return True, profit  

    #             elif current_price < enter_price:
    #                 if current_price <= enter_price - atr*self.s_l:
    #                     # print('hi3')
    #                     self.counter = 0
    #                     self.tralling_flag = False
    #                     profit = (current_price - enter_price)*qnt
    #                     return True, profit
                    
    #         if defender == -1: 
    #             self.checkpoint = enter_price*(1 - self.counter/100)
    #             self.tralling_s_l = enter_price - ((enter_price - self.checkpoint)/2)
    #             if current_price < enter_price:
    #                 if current_price <= self.checkpoint:
    #                     self.tralling_flag = True
    #                     self.counter += 1
    #                     if self.counter == 2:
    #                         self.counter = 0
    #                         # print('realy i am here')
    #                         self.tralling_flag = False
    #                         profit = (enter_price - current_price)*qnt
    #                         return True, profit                 
    #                 if (current_price >= self.tralling_s_l) and self.tralling_flag:
    #                     self.counter = 0
    #                     # print('hi2')
    #                     self.tralling_flag = False
    #                     profit = (enter_price - current_price)*qnt
    #                     return True, profit  

    #             elif current_price > enter_price:                        
    #                 if current_price >= enter_price + atr*self.s_l:
    #                     # print('hi3')
    #                     self.counter = 0
    #                     self.tralling_flag = False
    #                     profit = (enter_price - current_price)*qnt
    #                     return True, profit
                    
    #         return False, profit 



# class SL_STRATEGYYY():
#     def __init__(self, sl_strategy_number, depo) -> None:
#         self.sl_strategy_number = sl_strategy_number 
#         self.depo = depo
#         self.t_p = None
#         self.s_l = None
#         self.trailing_s_l = None
#         self.counter = 1
#         self.tralling_flag = False
#         self.checkpoint = None
#         self.atr_period = 14  # Период для расчета ATR
#         self.atr_multiplier = 2.0  # Множитель для определения ATR-базированного трейлинг-стопа

#     # ... другие методы ...

#     def calculate_trailing_stop(self, defender, enter_price, current_price, atr):
#         trailing_stop = None

#         if defender == 1:
#             self.checkpoint = enter_price * (1 + (self.counter * (atr/10)))
#             trailing_stop = enter_price - atr * self.atr_multiplier

#             if current_price >= self.checkpoint:
#                 self.tralling_flag = True
#                 self.counter += 1
#                 if self.counter == 2:
#                     self.counter = 0
#                     self.tralling_flag = False
#             elif current_price <= trailing_stop and self.tralling_flag:
#                 self.counter = 0
#                 self.tralling_flag = False

#         elif defender == -1:
#             self.checkpoint = enter_price * (1 - (self.counter * (atr/10)))
#             trailing_stop = enter_price + atr * self.atr_multiplier

#             if current_price <= self.checkpoint:
#                 self.tralling_flag = True
#                 self.counter += 1
#                 if self.counter == 2:
#                     self.counter = 0
#                     self.tralling_flag = False
#             elif current_price >= trailing_stop and self.tralling_flag:
#                 self.counter = 0
#                 self.tralling_flag = False

#         return trailing_stop

#     def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt):
#         profit = None
#         self.s_l = 0.01

#         trailing_stop = self.calculate_trailing_stop(defender, enter_price, current_price, atr)

#         if defender == 1:
#             if current_price <= trailing_stop:
#                 profit = (current_price - enter_price) * qnt
#                 return True, profit
#         elif defender == -1:
#             if current_price >= trailing_stop:
#                 profit = (enter_price - current_price) * qnt
#                 return True, profit

#         return False, profit
    


#     def sl_strategy_one(self, defender, enter_price, current_price, qnt): 
#         profit = None
#         self.t_p = 0.0015
#         self.s_l = 0.001
#         # self.t_p = 0.015
#         # self.s_l = 0.007

#         if defender == 1:             
#             if current_price >= enter_price + enter_price*self.t_p:
#                 profit = (current_price - enter_price)*qnt
#                 return True, profit
#             if current_price <= enter_price - enter_price*self.s_l:
#                 profit = (current_price - enter_price)*qnt
#                 return True, profit
#         if defender == -1:                
#             if current_price <= enter_price - enter_price*self.t_p:
#                 profit = (enter_price - current_price)*qnt
#                 return True, profit
#             if current_price >= enter_price + enter_price*self.s_l:
#                 profit = (enter_price - current_price)*qnt
#                 return True, profit

#         return False, profit
        
#     def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt):
#             profit = None
#             self.s_l = 0.01
#             # print(defender, enter_price, current_price, atr, qnt)

#             if defender == 1: 
#                 self.checkpoint = enter_price*(1 + self.counter/100)
#                 self.tralling_s_l = enter_price + ((self.checkpoint - enter_price)/2)
#                 if current_price > enter_price:
#                     if current_price >= self.checkpoint:
#                         self.tralling_flag = True
#                         self.counter += 1
#                         if self.counter == 2:
#                             self.counter = 0
#                             # print('realy i am here')
#                             self.tralling_flag = False
#                             profit = (current_price - enter_price)*qnt
#                             return True, profit                   
#                     if (current_price <= self.tralling_s_l) and self.tralling_flag:
#                         self.counter = 0
#                         # print('hi2')
#                         self.tralling_flag = False
#                         profit = (current_price - enter_price)*qnt
#                         return True, profit  
#                     # if (current_price <= self.tralling_s_l):
#                     #     self.counter = 0
#                     #     print('hi4')
#                     #     self.tralling_flag = False
#                     #     profit = (current_price - enter_price)*qnt
#                     #     return True, profit  
#                 elif current_price < enter_price:
#                     if current_price <= enter_price - atr*self.s_l:
#                         # print('hi3')
#                         self.counter = 0
#                         self.tralling_flag = False
#                         profit = (current_price - enter_price)*qnt
#                         return True, profit
                    
#             if defender == -1: 
#                 self.checkpoint = enter_price*(1 - self.counter/100)
#                 self.tralling_s_l = enter_price - ((enter_price - self.checkpoint)/2)
#                 if current_price < enter_price:
#                     if current_price <= self.checkpoint:
#                         self.tralling_flag = True
#                         self.counter += 1
#                         if self.counter == 2:
#                             self.counter = 0
#                             # print('realy i am here')
#                             self.tralling_flag = False
#                             profit = (enter_price - current_price)*qnt
#                             return True, profit                 
#                     if (current_price >= self.tralling_s_l) and self.tralling_flag:
#                         self.counter = 0
#                         # print('hi2')
#                         self.tralling_flag = False
#                         profit = (enter_price - current_price)*qnt
#                         return True, profit  
#                     # if (current_price >= self.tralling_s_l):
#                     #     self.counter = 0
#                     #     print('hi4')
#                     #     self.tralling_flag = False
#                     #     profit = (enter_price - current_price)*qnt
#                     #     return True, profit  

#                 elif current_price > enter_price:                        
#                     if current_price >= enter_price + atr*self.s_l:
#                         # print('hi3')
#                         self.counter = 0
#                         self.tralling_flag = False
#                         profit = (enter_price - current_price)*qnt
#                         return True, profit
                    
#             return False, profit
    
#     def sl_strategy_three(self, defender, enter_price, current_price, atr, qnt):
#         profit = None
#         self.t_p = 0.015
#         self.s_l = 0.007
#         self.t_p = 0.0015
#         self.s_l = 0.001
        
#         if defender == 1:                
#             if current_price >= enter_price + atr*self.t_p:
#                 profit = (current_price - enter_price)*qnt
#                 return True, profit
#             if current_price <= enter_price - atr*self.s_l:
#                 profit = (current_price - enter_price)*qnt
#                 return True, profit
            
#         if defender == -1:                
#             if current_price <= enter_price - atr*self.t_p:
#                 profit = (enter_price - current_price)*qnt
#                 return True, profit
#             if current_price >= enter_price + atr*self.s_l:
#                 profit = (enter_price - current_price)*qnt
#                 return True, profit

#         return False, profit

# def serialize_analysis(obj):
#     if isinstance(obj, datetime):
#         return obj.isoformat()
#     return obj.__dict__

    # for key, item in all_coins_indicators.items():
    #     print(f"Symbol: {item.symbol}")
    #     for indicator, value in item.summary.items():
    #         print(f"{indicator}: {value}")
    #     print()
    # for key, item in all_coins_indicators.items():
    #     # Преобразование индикатора в формат JSON
    #     indicator_json = json.dumps(item, default=serialize_analysis, indent=4)
        
    #     # Вывод красиво отформатированного индикатора
    #     print(f"Indicator: {key}")
    #     print(indicator_json)
    #     print("-" * 40)


    # {'Recommend.Other': -0.09090909, 'Recommend.All': -0.17878788, 'Recommend.MA': -0.26666667, 'RSI': 44.81125255, 'RSI[1]': 43.29762683, 'Stoch.K': 28.66705173, 'Stoch.D': 23.56146293, 'Stoch.K[1]': 23.80927336, 'Stoch.D[1]': 23.33301146, 'CCI20': -81.05682515, 'CCI20[1]': -89.18811541, 'ADX': 18.44619353, 'ADX+DI': 21.95399191, 'ADX-DI': 17.70659088, 'ADX+DI[1]': 22.91660192, 'ADX-DI[1]': 18.48296638, 'AO': -0.01047176, 'AO[1]': -0.00950353, 'Mom': -0.0045, 'Mom[1]': -0.0059, 'MACD.macd': -0.00253777, 'MACD.signal': -0.00153735, 'Rec.Stoch.RSI': 0, 'Stoch.RSI.K': 23.33070184, 'Rec.WR': 0, 'W.R': -65.56603774, 'Rec.BBPower': 0, 'BBPower': -0.00568501, 'Rec.UO': 0, 'UO': 44.85063613, 'close': 0.231, 'EMA5': 0.23084562, 'SMA5': 0.2293, 'EMA10': 0.23246901, 'SMA10': 0.23237, 'EMA20': 0.23510024, 'SMA20': 0.236425, 'EMA30': 0.23567327, 'SMA30': 0.23866333, 'EMA50': 0.23341322, 'SMA50': 0.237706, 'EMA100': 0.22614021, 'SMA100': 0.221623, 'EMA200': 0.22034421, 'SMA200': 0.2133835, 'Rec.Ichimoku': 0, 'Ichimoku.BLine': 0.23885, 'Rec.VWMA': -1, 'VWMA': 0.23668692, 'Rec.HullMA9': 1, 'HullMA9': 0.22825556, 'Pivot.M.Classic.S3': 0.04233333, 'Pivot.M.Classic.S2': 0.14623333, 'Pivot.M.Classic.S1': 0.19526667, 'Pivot.M.Classic.Middle': 0.25013333, 'Pivot.M.Classic.R1': 0.29916667, 'Pivot.M.Classic.R2': 0.35403333, 'Pivot.M.Classic.R3': 0.45793333, 'Pivot.M.Fibonacci.S3': 0.14623333, 'Pivot.M.Fibonacci.S2': 0.18592313, 'Pivot.M.Fibonacci.S1': 0.21044353, 'Pivot.M.Fibonacci.Middle': 0.25013333, 'Pivot.M.Fibonacci.R1': 0.28982313, 'Pivot.M.Fibonacci.R2': 0.31434353, 'Pivot.M.Fibonacci.R3': 0.35403333, 'Pivot.M.Camarilla.S3': 0.2157275, 'Pivot.M.Camarilla.S2': 0.22525167, 'Pivot.M.Camarilla.S1': 0.23477583, 'Pivot.M.Camarilla.Middle': 0.25013333, 'Pivot.M.Camarilla.R1': 0.25382417, 'Pivot.M.Camarilla.R2': 0.26334833, 'Pivot.M.Camarilla.R3': 0.2728725, 'Pivot.M.Woodie.S3': 0.08845, 'Pivot.M.Woodie.S2': 0.144775, 'Pivot.M.Woodie.S1': 0.19235, 'Pivot.M.Woodie.Middle': 0.248675, 'Pivot.M.Woodie.R1': 0.29625, 'Pivot.M.Woodie.R2': 0.352575, 'Pivot.M.Woodie.R3': 0.40015, 'Pivot.M.Demark.S1': 0.2227, 'Pivot.M.Demark.Middle': 0.26385, 'Pivot.M.Demark.R1': 0.3266, 'open': 0.2297, 'P.SAR': 0.24637133, 'BB.lower': 0.22512954, 'BB.upper': 0.24772046, 'AO[2]': -0.00973471, 'volume': 669125.23, 'change': 0.56595559, 'low': 0.2281, 'high': 0.2331}

# Total: 1.296819999999974$ 
# Win_per: 100.0%

            # # print(item.oscillators)
            # print(item.indicators)

                # try:
                #     # print(main_stake)
                #     main_stake = bin_data.get_klines(main_stake)
                #     print(main_stake)
                #     qq = 0
                #     for item in main_stake:
                #         item["atr"] = calculate_atr(item["klines"])
                #         item["qnt"], recalculated_depo = calc_qnt_func(item, my_params.depo)
                #         # print(recalculated_depo)
                #         try:
                #             qq = item["atr"] / item["atr_1"]
                #             atr_corrector_list.append(qq)
                #         except:
                #             pass
                         
                #         del item["klines"]
                    
                #     atr_corrector = sum(atr_corrector_list) / len(atr_corrector_list) 
                #     print(main_stake)
                #     print(atr_corrector)
                # except Exception as ex:
                #     print(f"main__233:\n{ex}") 
                # sys.exit()

            # print(item.oscillators)
            # print(item.indicators)


# import shutil
# import tempfile

# def cleanup_cache():
#     import os
#     try:

        
#         cache_dir = tempfile.mkdtemp()
#     except Exception as ex:
#         # print(f"386____{ex}")
#         pass    
#     try:
#         if os.path.exists("__pycache__"):
#             shutil.rmtree("__pycache__")
#     except Exception as ex:
#         # print(f"392____{ex}")
#         pass    
#     try:
#         if os.path.exists(cache_dir):
#             shutil.rmtree(cache_dir)
#     except Exception as ex:
#         # print(f"396____{ex}")
#         pass


            # elif self.sl_strategy_number == 1:
            #     profit_flag, profit = self.sl_strategy_one(defender, enter_price, current_price, qnt)
            #     if profit_flag:
            #         item['close_order'] = True  
            #     item['profit'] = profit

            # elif self.sl_strategy_number == 3:
            #     profit_flag, profit = self.sl_strategy_three(defender, enter_price, current_price, atr, qnt) 
            #     if profit_flag:
            #         item['close_order'] = True   
            #     item['profit'] = profit


        # if self.market == 'futures':
        #     response = self.spot_client.futures_create_order(**params)
        # elif self.market == 'futures':
        #     response = self.futures_client.new_order(**params)
        # else:
        #     raise ValueError("Invalid market type")


# from API.config import Configg
# from pparamss import my_params

# class CREATE_BINANCE_ORDER(Configg):

#     def __init__(self, market, test_flag) -> None:
#         super().__init__(market=market, test_flag=test_flag)

#     def open_order(self,):
#         pass

#     def close_order(self,):
#         pass

# create_orders_obj = CREATE_BINANCE_ORDER()

# symbol = 'BTCUSDT'
# quantity = 1.0
# price = 50000
# side = 'BUY'
# order_type = 'LIMIT'

# order_type = 'MARKET'

# # Open an order
# response = create_orders_obj.open_order(symbol, quantity, price, side, order_type)
# print("Opened Order:", response)

# # Close an order
# order_id = response['orderId']  # You can get the order ID from the response when opening the order
# close_response = create_orders_obj.close_order(symbol, order_id)
# print("Closed Order:", close_response)

# order_id = response.get('orderId')

# response = self.futures_client.new_order(**params)

                        # all_tickers = self.futures_client.ticker_24hr_price_change()


# import os
# from dotenv import load_dotenv

# from binance.client import Client
# from binance.um_futures import UMFutures
# import hmac 
# import hashlib 
# import requests
# # pip install python-dotenv

# load_dotenv()

# class Configg():

#     api_key, api_secret = None, None
#     spot_client, futures_client = None, None
#     header = None

#     def __init__(self, market, test_flag) -> None:  
#         # if market == 'spot':
#         self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_SPOT", "")
#         # print(self.api_key)
#         self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_SPOT", "")
#         # print(self.api_secret)
#         self.spot_client = Client(self.api_key, self.api_secret)
#         # print(self.spot_client)
#         # if market == 'futures':
#         #     self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_FUTURES", "")
#         #     self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_FUTURES", "")  
#         #     self.futures_client = UMFutures(self.api_key, self.api_secret)
             
#         self.market = market    
#         self.test_flag = test_flag

#         self.header = {
#             'X-MBX-APIKEY': self.api_key
#         }

#     def get_signature(self, params):
#         import time
#         params['timestamp'] = int(time.time() *1000)
#         params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
#         hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
#         params['signature'] = hash.hexdigest()
        
#         return params
    
#     def HTTP_request(self, url, **kwards):
#         responce = None
#         try:
#             responce = requests.request(url=url, **kwards)
#             responce = responce.json()  
#         except Exception as ex:
#             print(ex) 
#         # print(responce.status_code)
#         # print(responce.json())
#         return responce

# # python -m API.config

        # elif my_params.main_strategy_number == 2:
        #     repl = None
        #     symbol = data
        #     repl = self.get_klines_helper(symbol)
        #     return repl