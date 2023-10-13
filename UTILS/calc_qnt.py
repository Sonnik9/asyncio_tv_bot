# def calc_qnt_func(main_stake):
from pparamss import my_params
import requests
import logging
import os
import inspect
import math 
logging.basicConfig(filename='my_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

def get_symbol_info(symbol):    
    data = None
    response = None
    url = f"{my_params.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"

    try:
        response = requests.get(url)
        data = response.json() 
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

    return data

def calc_qnt_func(symbol, enter_price, depo):    

    symbol_info = None
    symbol_data = None 
    quantity = None 

    symbol_info = get_symbol_info(symbol)

    if symbol_info:
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

    if symbol_data:    
        step_size = float(symbol_data['filters'][1]['stepSize'])
        if my_params.MARKET == 'spot':
            min_notional = float(symbol_data['filters'][6]['minNotional'])
        else:
            min_notional = float(symbol_data['filters'][5]['notional'])

        for _ in range(5):
            quantity = depo / enter_price    
            quantity = round(quantity / step_size) * step_size
            if quantity * enter_price < min_notional:                 
                depo = depo + depo * 0.2  
                quantity = None   
                continue
            else:                
                # recalculated_depo = quantity * enter_price
                break

    return quantity



# def calc_qnt_func(symbol, enter_price, depo):    
#     symbol_info = None
#     symbol_data = None 
#     quantity, recalculated_depo = None, None
#     symbol_info = get_symbol_info(my_params.market, symbol)
#     if symbol_info:
#         symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

#     if symbol_data:
#         step_size = float(symbol_data['filters'][1]['stepSize'])
#         if my_params.market == 'spot':
#             min_notional = float(symbol_data['filters'][6]['minNotional'])
#         elif my_params.market == 'futures':
#             min_notional = float(symbol_data['filters'][5]['notional'])

#         price_precision = abs(int(math.log10(step_size)))
#         quantity_precision = abs(int(math.log10(1 / min_notional)))

#         for _ in range(4):            
#             quantity = depo / enter_price    
#             quantity = round(quantity / step_size, quantity_precision) * step_size
#             if quantity * enter_price < min_notional:                 
#                 depo = depo + depo * 0.2  
#                 quantity = None   
#                 continue
#             else:                
#                 recalculated_depo = quantity * enter_price
#                 break

#     return quantity, recalculated_depo
