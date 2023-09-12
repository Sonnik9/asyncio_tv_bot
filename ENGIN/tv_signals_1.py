# from tradingview_ta import TA_Handler, Interval, Exchange
from tradingview_ta import *
from pparamss import my_params

class TV_STRONG_SIGNALS():

    def __init__(self)-> None:
        pass

    def get_tv_signals(self, top_coins, interval):
        all_coins_indicators = None
        orders_stek = None
        symbols = [f"BINANCE:{x}" for x in top_coins if x]

        all_coins_indicators = get_multiple_analysis(symbols=symbols,
                            screener='crypto',                    
                            interval=interval)
        try:
            orders_stek = self.sigmals_analizator(all_coins_indicators)
        except Exception as ex:
            print(ex)

        return orders_stek

    def sigmals_analizator(self, all_coins_indicators):
        orders_stek = []
        recommendation = None
        indicator = None
        for _, item in all_coins_indicators.items():
            try:
                indicator = item.symbol
                recommendation = item.summary["RECOMMENDATION"]
            except Exception as ex:
                pass
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

get_orders_stek = TV_STRONG_SIGNALS()
