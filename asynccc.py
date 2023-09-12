import websockets
import asyncio
import json
from MONEY.stop_logic_1 import tp_sl_strategy_1_func

async def price_monitoring(symbol, defender):
    url = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1s'
    profit = None
    close_position = False
    qnt = 0.001
    first_price_flag = False
    async with websockets.connect(url) as websocket:      

        try:
            async for message in websocket:
                data = json.loads(message)
                print(f"{data['s']}:  {data['k']['c']}")
                if not first_price_flag:
                    enter_price = float(data['k']['c'])
                    first_price_flag = True
                    continue
                else:
                    current_price = float(data['k']['c'])
                    profit, close_position = tp_sl_strategy_1_func(enter_price, current_price, qnt, defender)

                    await asyncio.sleep(5)
                
                if close_position:
                    return profit, symbol
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await websocket.close()

    return profit

async def shell_monitiringg(symbol, defender):
    profit = None
    profit, symbol = await price_monitoring(symbol, defender)
    
    return profit, symbol

