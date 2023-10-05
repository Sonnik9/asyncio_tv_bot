from tradingview_ta import *
from pparamss import my_params

def sigmals_handler_one(all_coins_indicators):
    orders_stek = []
    recommendation = None
    indicator = None

    for _, item in all_coins_indicators.items():
        try:            
            # print(item.oscillators)
            # print(item.indicators)
            indicator = item.symbol
            recommendation = item.summary["RECOMMENDATION"]
        except Exception as ex:
            pass
            # print(ex)
        if recommendation == 'STRONG_BUY':
            try:
                orders_stek.append((indicator, 1))          
            except:
                pass
        elif recommendation == 'STRONG_SELL':  
            try:          
                orders_stek.append((indicator, -1))             
            except:
                pass

    return orders_stek 


