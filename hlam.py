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
