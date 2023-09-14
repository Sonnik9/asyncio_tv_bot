import asyncio
import time
from API.bin_data_get import bin_data
from pparamss import my_params
from ENGIN.tv_signals_1 import get_orders_stek
from UTILS.waiting_candle import kline_waiter
from MONEY.asumm import asum_counter
from MONEY.stop_logic_1 import sl_tp_logic
from ENGIN.tv_signals_1 import get_orders_stek
from pparamss import my_params
from API.bin_data_get import bin_data
import pytz
from datetime import datetime, time
# import websockets
import asyncio
import aiohttp
import json
# import sys

# stake_list_lock = asyncio.Lock()
# current_stake_list = set()
# profit_variable_lock = asyncio.Lock()
# profit_list = []

async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='      
    # streams = []
    print(main_stake)
    streams = [f"{k['symbol'].lower()}@kline_1s" for k in main_stake]
    # print(streams)
    # return
        
    try:
        while True:   
            data_prep = None   
            ws = None            
            iterr_flag = False
            intermedeate_data_list = []    
            enter_list = []
            new_formated_data = []    
            try:
                print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 7
                        }
                        try:
                            data_prep = await ws.send_json(subscribe_request)                            
                        except:
                            pass
                   
                        if not data_prep and iterr_flag:                                                
                            await asyncio.sleep(7)
                            continue
                        
                        async for msg in ws:                            
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:                                    
                                    data = json.loads(msg.data)                                                            
                                    symbol = data.get('data',{}).get('s')                                    
                                    close_price = float(data.get('data',{}).get('k',{}).get('c'))                                    
                                    intermedeate_data_list.append((symbol, close_price))                                                        
                                except:
                                    pass

                                if len(intermedeate_data_list) == len(streams):
                                    if not iterr_flag:                                        
                                        enter_list = intermedeate_data_list
                                        iterr_flag = True
                                        intermedeate_data_list = []
                                        continue
                                    new_formated_data = await data_callback(intermedeate_data_list, enter_list, main_stake)
                                    intermedeate_data_list = []
                                    # print(new_formated_data)           
                                    main_stake = sl_tp_logic(new_formated_data)
                                    
                                    # await asyncio.sleep(5)
                                    if main_stake:
                                        return main_stake

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)
                continue
    except:
        pass
    finally:
        await ws.close()
        return main_stake

async def process_data(data_list, enter_list, main_stake):
    formated_data = []
    new_formated_data = []

    for symbol, current_price in data_list:  
        for s, d in main_stake:
            if symbol==s:
                formated_data.append((symbol, d, current_price))
                break
    for symboll, enter_pr in enter_list:
        for symbo, deff, cur_pr in formated_data:
            if symboll == symbo:
                new_formated_data.append((symboll, enter_pr, cur_pr, deff))
                break
    
    # print(new_formated_data)
    # print(formated_data)
    # print('/'*100)
    return new_formated_data

def stake_generator(usual_defender_stake):
    universal_stake = [
        {
            "profit": None,
            "symbol": s,
            "defender": d,
            "enter_price": None,
            "current_price": None,
            "in_position": False,
            "close_order": False
        }
            for s, d in usual_defender_stake
    ] 

    return universal_stake

async def main():
    first_flag = True
    top_coins = None  
    usual_defender_stake = None 
    total_raport_list = [] 
    intermedeate_raport_list = [] 

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
            # await asyncio.sleep(2)
            now = datetime.now()
            desired_timezone = pytz.timezone('Europe/Kiev')
            now_in_desired_timezone = now.astimezone(desired_timezone)
            current_time = now_in_desired_timezone.strftime('%H:%M')
            print(current_time)
            if time(21, 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(23, 0):
                print('it is time to assuming!')                
                asum_counter(total_raport_list)
                break
            try:
                usual_defender_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)
            except Exception as ex:
                print(ex) 

            if not usual_defender_stake:
                await asyncio.sleep(5)
                continue

            if first_flag:                              
                if len(usual_defender_stake) > my_params.max_threads:
                    usual_defender_stake = usual_defender_stake[:my_params.max_threads]
                universal_stake = stake_generator(usual_defender_stake)
                main_stake = universal_stake
                first_flag = False  
            else:
                decimal = my_params.max_threads - len(main_stake)
                if len(usual_defender_stake) > decimal:
                    usual_defender_stake = usual_defender_stake[:decimal]
                universal_stake = stake_generator(usual_defender_stake)
                main_stake = main_stake + universal_stake
              
            # ///////////////////////////////////////////////////////////////////////
            try:
                main_stake = await price_monitoring(main_stake, process_data)
                if main_stake:                         
                    intermedeate_raport_list = [x for x in main_stake if x["close_order"]] 
                    total_raport_list += intermedeate_raport_list
                    main_stake = [x for x in main_stake if not x["close_order"]]
                # break
            except Exception as ex:
                print(f"main__192:\n{ex}")         

        except Exception as ex:
            print(f"main__195:\n{ex}")
            await asyncio.sleep(5)
   
    
    print("There was a good!")

if __name__ == "__main__":
    asyncio.run(main())
