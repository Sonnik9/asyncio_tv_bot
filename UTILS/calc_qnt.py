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

def calc_qnt_func(symbol, price, depo): 

    symbol_info = None
    symbol_data = None 
    quantity = None
    symbol_info = get_symbol_info(symbol)
    # print(symbol_info)
    if symbol_info:
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

    if symbol_data:
        step_size = float(symbol_data['filters'][1]['stepSize'])
        if my_params.MARKET == 'spot':
            min_notional = float(symbol_data['filters'][6]['minNotional'])
        elif my_params.MARKET == 'futures':
            min_notional = float(symbol_data['filters'][5]['notional'])

        # price_precision = abs(int(math.log10(step_size)))
        quantity_precision = abs(int(math.log10(1 / min_notional)))

        decimal = depo * 0.2

        for _ in range(5):
            quantity = depo / price  
            try:  
                quantity = round((round(quantity / step_size, quantity_precision) * step_size), quantity_precision)
            except:
                ('her ai am')

            if quantity * price < min_notional:                 
                depo = depo + decimal  
                quantity = None   
                continue
            else:               
                break
    # print(quantity)
    return quantity
