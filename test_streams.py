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

import aiohttp
import asyncio
import json

async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='
    profit = None
    close_position = False
    qnt = 0.001
    first_price_flag = False
    ws = None
    streams = [f'{item[0].lower()}@kline_1s' for item in main_stake]
    # streams = ['agldusdt@kline_1s', 'zecusdt@kline_1s', 'rndrusdt@kline_1s', 'iotxusdt@kline_1s', 'galusdt@kline_1s', 'runeusdt@kline_1s', 'trbusdt@kline_1s']
    try:
        while True:                
            try:
                print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 87
                        }
                        await ws.send_json(subscribe_request)

                        data_list = []
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    data = json.loads(msg.data)                            
                                    symbol = data.get('data',{}).get('s')
                                    close_price = float(data.get('data',{}).get('k',{}).get('c'))
                                    data_list.append((symbol, close_price))
                                except:
                                    pass

                                if len(data_list) == len(streams):
                                    await data_callback(data_list, main_stake)
                                    data_list = []

            except aiohttp.ClientError as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)  
                continue
            except ws.exceptions.ConnectionClosed:
                await asyncio.sleep(7)  
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)
                continue
    except:
        pass
    finally:
        await ws.close()

async def process_data(data_list, main_stake):
    # print(data_list)
    # print('/'*20)
    formated_price_list = []
    for symbol, close_price in data_list:
        for s, d in main_stake:
            if symbol==s:
                formated_price_list.append(symbol, d, close_price)
                break
    
    print(formated_price_list)
    print('/'*100)


