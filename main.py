import asyncio
import time
from API.bin_data_get import bin_data
from pparamss import my_params
from ENGIN.tv_signals_1 import get_orders_stek
from UTILS.waiting_candle import kline_waiter
from taskss import setup_tasks
import sys

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
            first_added_stake = []
            first_stake = get_orders_stek.get_tv_signals(top_coins, my_params.interval)            
            if first_stake:
                break
                # first_stake = first_stake[:2]
            else:
                await asyncio.sleep(5)
        except Exception as ex:
            print(f"main__39:\n{ex}")
    try:
        first_stake = first_stake[:2]
        
        if len(first_stake) > my_params.max_threads:
            first_stake = first_stake[:my_params.max_threads]
        
        if len(first_stake) < my_params.max_threads:
            for _ in range(my_params.max_threads - len(first_stake)):
                first_added_stake.append((None, None))
            first_stake += first_added_stake
        print(first_stake)
        await setup_tasks(first_stake)
    except Exception as ex:
        print(f"main__51:\n{ex}")
    
    
    print("The first_stake was launched successfully!")

if __name__ == "__main__":
    asyncio.run(main())
