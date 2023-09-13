import asyncio
import time
from API.bin_data_get import bin_data
from pparamss import my_params
from ENGIN.tv_signals_1 import get_orders_stek
from UTILS.waiting_candle import kline_waiter
from ENGIN.tv_signals_1 import get_orders_stek
from pparamss import my_params
from API.bin_data_get import bin_data
import pytz
from datetime import datetime, time
# import websockets
import asyncio
import aiohttp
import json
import sys
from MONEY.stop_logic_1 import tp_sl_strategy_1_func

# counter_variable_lock = asyncio.Lock()
# counter_var = 0



stake_list_lock = asyncio.Lock()
current_stake_list = set()
profit_variable_lock = asyncio.Lock()
profit_list = []




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


async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='
    profit = None
    close_position = False
    first_iter = False
    streams = []
    streams = [f'{item[0].lower()}@kline_1s' for item in main_stake]

    try:
        while True:   
            data_prep = None   
            ws = None
            data_list = []        
            try:
                print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 87
                        }
            
                        data_prep = await ws.send_json(subscribe_request)
                        if not data_prep and first_iter:                            
                            await asyncio.sleep(7)

                        async for msg in ws:
                            first_iter = True
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

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)
                continue
    except:
        pass
    finally:
        await ws.close()
        return profit, close_position

async def process_data(data_list, main_stake):
    formated_price_list = []
    for symbol, close_price in data_list:
        for s, d in main_stake:
            if symbol==s:
                formated_price_list.append((symbol, d, close_price))
                break
    
    print(formated_price_list)
    print('/'*100)

async def main():
    # sys.exit()
    # loop = asyncio.get_event_loop()
    # loop.close()
    top_coins = None    
    try:
        top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins)
    except Exception as ex:
        print(f"main__15:\n{ex}")    
    # print(top_coins)    
    try:
        wait_time = kline_waiter(my_params.kline_time, my_params.time_frame)
        print(f"waiting time to close last candle is: {wait_time} sec")
        # await asyncio.sleep(wait_time)
    except Exception as ex:
        print(f"main__24:\n{ex}")
    
    while True:
        try:
            first_stake = []            
            first_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)            
            if first_stake:
                break
            else:
                await asyncio.sleep(5)
        except Exception as ex:
            print(f"main__39:\n{ex}")
            await asyncio.sleep(5)
    try:
        # first_stake = first_stake[:2]
        first_added_stake = []
        
        if len(first_stake) > my_params.max_threads:
            first_stake = first_stake[:my_params.max_threads]
        
        # if len(first_stake) < my_params.max_threads:
        #     for _ in range(my_params.max_threads - len(first_stake)):
        #         first_added_stake.append((None, None))
        #     first_stake += first_added_stake
        print(first_stake)
        await price_monitoring(first_stake, process_data)
    except Exception as ex:
        print(f"main__51:\n{ex}")
    
    
    print("The first_stake was launched successfully!")

if __name__ == "__main__":
    asyncio.run(main())
