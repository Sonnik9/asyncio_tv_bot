import asyncio
# import time
# import websockets
from API.bin_data_get import bin_data
from API.create_order import create_orders_obj
from pparamss import my_params
from ENGIN.main_strategy_controller import strateg_controller
   
from UTILS.waiting_candle import kline_waiter
# from UTILS.indicators import calculate_atr
# from UTILS.calc_qnt import calc_qnt_func
from UTILS.clean_cashe import cleanup_cache
from MONEY.asumm import asum_counter
from MONEY.stop_logic import sl_strategies
from pparamss import my_params
from API.bin_data_get import bin_data
import pytz
from datetime import datetime, time
import asyncio
import aiohttp
import json
import sys 

# stake_list_lock = asyncio.Lock()
# current_stake_list = set()
# profit_variable_lock = asyncio.Lock()
# profit_list = []

async def price_monitoring(main_stakee, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='      
    # streams = []
    # print(main_stake)
    returning_main_stake = []
    streams = [f"{k['symbol'].lower()}@kline_1s" for k in main_stakee]
    print(f"start_stake:___{len(main_stakee)}")
    # print(streams)
    # return
        
    try:
        while True:   
            data_prep = None   
            ws = None            
            iterr_flag = False
            profit_flag = False
            intermedeate_data_list = []    
            enter_price_list = []
              
            try:
                # print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 94859867947
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
                                    # print(data)                                                          
                                    symbol = data.get('data',{}).get('s')                                    
                                    close_price = float(data.get('data',{}).get('k',{}).get('c'))   
                                    # print(close_price) s                                
                                    intermedeate_data_list.append((symbol, close_price))                                                    
                                except:
                                    pass

                                if len(intermedeate_data_list) == len(streams):
                                    if not iterr_flag:                                        
                                        enter_price_list = intermedeate_data_list
                                        iterr_flag = True
                                        intermedeate_data_list = []
                                        continue
                                    main_stakee, profit_flag = await data_callback(intermedeate_data_list, enter_price_list, main_stakee)
                                    intermedeate_data_list = []
                                    # await asyncio.sleep(5)
                                    if profit_flag:    
                                        returning_main_stake = main_stakee                                   
                                        return 

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)
                continue
    except:
        pass
    finally:
        await ws.close()
        return returning_main_stake
    
async def process_data(intermediate_data_list, enter_price_list, main_stake):
    # print(f"process_data_enter_price_list:__{len(enter_price_list)}")
    # print(f"process_data_intermediate_data_list:__{len(enter_price_list)}")
    # print(f"process_data_main_stake_before:__{len(main_stake)}")
    # print(enter_price_list)

    symbol_to_item = {item['symbol']: item for item in main_stake}    
    profit_flag = False
    for symbol, current_price in intermediate_data_list:
        if symbol in symbol_to_item:
            symbol_to_item[symbol]['current_price'] = current_price

    for symbol, enter_price in enter_price_list:
        if symbol in symbol_to_item and not symbol_to_item[symbol]['in_position']:
            symbol_to_item[symbol]['enter_price'] = enter_price

    main_stake = list(symbol_to_item.values())
    # print(main_stake)

    try:
        main_stake, profit_flag = sl_strategies.sl_controller(main_stake)
    except Exception as ex:
        print(f"125:__{ex}")

    return main_stake, profit_flag

def stake_generator(usual_defender_stake):
    universal_stake = [
        {
            "profit": None,
            "symbol": s,
            "defender": d,
            "enter_price": None,
            "current_price": None,
            "range_counter": 1,
            "in_position": False,
            "close_order": False,
            "atr": atr,
            "atr_a": atr_a
        }
            for s, d, atr, atr_a in usual_defender_stake            
    ] 

    return universal_stake

async def main():
    first_flag = True
    top_coins = []  
    usual_defender_stake = []
    total_raport_list = [] 
    intermedeate_raport_list = [] 
    main_stake_symbols_list = []
    recalculated_depo = None
    atr_corrector_list = []
    # print(my_params.limit_selection_coins)
    try:
        top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins)
    except Exception as ex:
        print(f"main__15:\n{ex}")    
    print(len(top_coins)) 

    # sys.exit() 
    try:
        wait_time = kline_waiter(my_params.kline_time, my_params.time_frame)
        print(f"waiting time to close last candle is: {wait_time} sec")
        # await asyncio.sleep(wait_time)
    except Exception as ex:
        print(f"main__24:\n{ex}")
    
    while True:
        try:
            # await asyncio.sleep(2)
            if len(total_raport_list) >= 4:
                print('it is time to assuming!')  
                asum_counter(total_raport_list)
                create_orders_obj.cancel_all_orderss()
                cleanup_cache()
                break

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
                usual_defender_stake = strateg_controller.main_strategy_control_func(top_coins)
                print(len(usual_defender_stake))
                usual_defender_stake = [x for x in usual_defender_stake if x[0] not in main_stake_symbols_list]
                # print(usual_defender_stake)
            except Exception as ex:
                print(f"192___{ex}") 
            try:
                if len(usual_defender_stake) == 0:
                    await asyncio.sleep(5)
                    continue
                else:
                    if first_flag:                                            
                        if len(usual_defender_stake) > my_params.max_threads:
                            usual_defender_stake = usual_defender_stake[:my_params.max_threads]
                        universal_stake = stake_generator(usual_defender_stake)
                        main_stake = universal_stake
                        first_flag = False  
                    else:
                        try:
                            decimal = my_params.max_threads - len(main_stake)
                            if len(usual_defender_stake) > decimal:
                                usual_defender_stake = usual_defender_stake[:decimal]
                            universal_stake = stake_generator(usual_defender_stake)
                            main_stake = main_stake + universal_stake
                        except Exception as ex:
                            print(f"212___{ex}") 
            except Exception as ex:
                print(f"214___{ex}") 
              
            # ///////////////////////////////////////////////////////////////////////
            try:
                # print(main_stake)
                # sys.exit()
                main_stake = await price_monitoring(main_stake, process_data)
                if main_stake:                         
                    intermedeate_raport_list = [x for x in main_stake if x["close_order"]] 
                    total_raport_list += intermedeate_raport_list
                    main_stake = [x for x in main_stake if not x["close_order"]]
                    main_stake_symbols_list = [x['symbol'] for x in main_stake]
                    # print(total_raport_list)
                # break
            except Exception as ex:
                print(f"main__192:\n{ex}")         

        except Exception as ex:
            print(f"main__195:\n{ex}")
            await asyncio.sleep(5)
   
    
    print("There was a good!")

if __name__ == "__main__":
    # try:
    #     atexit.register(cleanup_cache)
    # except Exception as ex:
    #     print(f"461____{ex}")
    asyncio.run(main())
    sys.exit()

# killall -9 python
# killall -r /path/to/.venv

