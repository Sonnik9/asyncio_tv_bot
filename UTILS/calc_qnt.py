# def calc_qnt_func(main_stake):
from pparamss import my_params
import requests
import logging
import os
import inspect
logging.basicConfig(filename='my_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

def get_symbol_info(market, symbol):
    # import json
    data = None
    response = None

    if market == 'spot':
        url = f'https://testnet.binance.vision/api/v3/exchangeInfo?symbol={symbol}'
    else:
        url = f'https://testnet.binancefuture.com/fapi/v1/exchangeInfo?symbol={symbol}'
    try:
        response = requests.get(url)
        data = response.json() 
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

    return data

def calc_qnt_func(item, depo):
    # print(item)
    market, symbol, enter_price = my_params.market, item["symbol"], item["klines"]['Close'].iloc[-1]
    # print(enter_price)

    # print(symbol, depo, enter_price)
    symbol_info = None
    symbol_data = None 
    quantity, recalculated_depo = None, None
    symbol_info = get_symbol_info(market, symbol)
    if symbol_info:
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
    
    # if symbol_data is None:
    #     raise ValueError(f'Символ {symbol} не найден в списке символов')
    # else:
    #     print(f'Символ {symbol} есть в списке символов')

    if symbol_data:    
        step_size = float(symbol_data['filters'][1]['stepSize'])
        if market == 'spot':
            min_notional = float(symbol_data['filters'][6]['minNotional'])
        else:
            min_notional = float(symbol_data['filters'][5]['notional'])
        quantity = depo / enter_price    
        quantity = round(quantity / step_size) * step_size
        if quantity * enter_price < min_notional:
            raise ValueError('Депозит недостаточен для совершения сделки')
        
        # Пересчитанный размер депозита в зависимости от количества
        recalculated_depo = quantity * enter_price
    
    return quantity, recalculated_depo