import threading
import time
import asyncio 
import queue
from asynccc import shell_monitiringg
from ENGIN.tv_signals_1 import get_orders_stek
from pparamss import my_params
from API.bin_data_get import bin_data
stake_list_lock = asyncio.Lock()
current_stake_list = set()

async def tasks_controller(symbol, defender):
    profit = None

    try:
        async with stake_list_lock:
            current_stake_list.add(symbol)
        profit, symbol_to_remove = await shell_monitiringg(symbol, defender)
        print(f"tasks_19:___{profit}")
    except Exception as ex:
        print(ex)
    finally:
        async with stake_list_lock:
            current_stake_list.remove(symbol_to_remove)


async def setup_tasks(initial_stake):
    tasks = []
    # print(first_order_stake)
    for symbol, defender in initial_stake:
        if symbol:
            asyncio.create_task(tasks_controller(symbol, defender))
    
    # for symbol, defender in first_order_stake:
    #     task = asyncio.create_task(tasks_controller(symbol, defender))
    #     tasks.append(task)
    
    # await asyncio.gather(*tasks)



    # if symbol:
    #     current_stake_list.add(symbol)
    #     try:
    #         # print(symbol, defender)
    #         profit, symbol_to_remove = await shell_monitiringg(symbol, defender)
    #         print(f"tasks_20:___{profit}")
    #     except Exception as ex:
    #         print(ex)
    #     if profit:
    #         current_stake_list.remove(symbol_to_remove)
    #         symbol = None

    # if not symbol:

    #     while True: 
    #         print('Я в цикле!')  
    #         var_symbol, var_defender = None, None
    #         if len(current_stake_list) < my_params.max_threads:
    #             print('Прошел условие в цикле!') 
    #             # print(f"current_stake_list.set:___{list(current_stake_list)}")
    #             symbol_in_deal = False
    #             try:
    #                 top_coins = bin_data.all_tickers_func(my_params.limit_selection_coins) 
    #                 # print(top_coins) 
    #                 next_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)
    #                 # print(next_stake)
    #                 # break
    #             except Exception as ex:
    #                 print(ex)
    #             if next_stake:       
    #                 for symboll, defenderr in next_stake:                            
    #                     if symboll not in current_stake_list:
    #                         current_stake_list.add(symboll)
    #                         var_symbol, var_defender = symboll, defenderr                     
    #                         symbol_in_deal = True
    #                         break

    #                 if symbol_in_deal:
    #                     # print(var_symbol, var_defender)
    #                     try:
    #                         print(f"current_stake_list.set:___{current_stake_list}")
    #                         profit, symbol_to_remove = await shell_monitiringg(var_symbol, var_defender)
    #                         print(f"tasks_55:___{profit}")
                                                        
    #                     except Exception as ex:
    #                         print(ex)

    #                     if profit:
    #                         current_stake_list.remove(symbol_to_remove)
    #                         continue
    #                 else:
    #                     await asyncio.sleep(5)
    #                     continue

    #             else:
    #                 await asyncio.sleep(5)
    #                 continue
    #         else:
    #             await asyncio.sleep(5)
    #             continue