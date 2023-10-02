from UTILS import indicators

class IND_STR_TWO():

    def __init__(self) -> None:
        pass

    def bunch_handler_func(self, next_data, close_price, current_bunch):
        b_bband_q, s_bband_q, b_rsi_lev, s_rsi_lev, b_macd__q, s_macd_q, b_stoch_q, s_stoch_q = 1, 1, 33, 67, 1, 1, 23, 77

        signals_sum = []
        buy_signals_counter = 0
        sell_signals_counter = 0
        buy_total_signal, sell_total_signal = False, False

        if 'bband_flag' in current_bunch:
            upper, lower = indicators.calculate_bollinger_bands(next_data)        
            buy_bband_signal = close_price >= lower * b_bband_q
            sell_bband_signal = close_price <= upper * s_bband_q
            signals_sum.append((buy_bband_signal, sell_bband_signal))

        if 'macd_strong_flag' in current_bunch:
            macd, signal = indicators.calculate_macd(next_data)        
            buy_strong_macd_signal = (macd > signal * b_macd__q) & (macd < 0)
            sell_strong_macd_signal = (macd < signal * s_macd_q) & (macd > 0)
            signals_sum.append((buy_strong_macd_signal, sell_strong_macd_signal))

        if 'macd_lite_flag' in current_bunch:
            macd, signal = indicators.calculate_macd(next_data)        
            buy_lite_macd_signal = macd > signal * b_macd__q
            sell_lite_macd_signal = macd < signal * s_macd_q
            signals_sum.append((buy_lite_macd_signal, sell_lite_macd_signal))

        if 'rsi_flag' in current_bunch:
            rsi = indicators.calculate_rsi(next_data)        
            buy_rsi_signal = rsi <= b_rsi_lev
            sell_rsi_signal = rsi >= s_rsi_lev
            signals_sum.append((buy_rsi_signal, sell_rsi_signal))

        if 'stoch_flag' in current_bunch:
            fastk, slowk = indicators.calculate_stochastic_oscillator(next_data)        
            buy_stoch_signal = (fastk > slowk) & (fastk < b_stoch_q)
            sell_stoch_signal = (fastk < slowk) & (fastk > s_stoch_q)
            signals_sum.append((buy_stoch_signal, sell_stoch_signal))

        if 'engulfing_flag' in current_bunch:
            engulfing = indicators.calculate_engulfing_patterns(next_data)
            
            buy_engulfing_signal = engulfing > 0
            sell_engulfing_signal = engulfing < 0
            signals_sum.append((buy_engulfing_signal, sell_engulfing_signal))

        if 'doji_flag' in current_bunch:
            doji = indicators.calculate_doji(next_data)
            
            buy_doji_signal = doji != 0
            sell_doji_signal = doji != 0
            signals_sum.append((buy_doji_signal, sell_doji_signal))

        for buy_signal, sell_signal in signals_sum:
            if buy_signal:
                buy_signals_counter += 1
            if sell_signal:
                sell_signals_counter += 1

        if 'U' in current_bunch:
            if buy_signals_counter == len(signals_sum):
                buy_total_signal = True 
        if 'D':
            if sell_signals_counter == len(signals_sum):
                sell_total_signal = True
        if 'F' in current_bunch:
            if buy_signals_counter == len(signals_sum):
                buy_total_signal = True 
            if sell_signals_counter == len(signals_sum):
                sell_total_signal = True

        return buy_total_signal, sell_total_signal

    def trends_defender(self, next_data, close_price):

        try:
            adx = indicators.calculate_adx(next_data)        
            sma = indicators.calculate_sma(next_data)        
        except Exception as ex:
            print(ex)
        if close_price > sma and adx > 25:
            return "U"

        elif close_price < sma and adx > 25:
            return "D"
        else:
            return "F"

    def signal_gen(self, next_data, close_price): 
            bunch_variant = 2   
            
            buy_signal, sell_signal = False, False
            trende_sign = self.trends_defender(next_data, close_price)
                        
            if trende_sign == 'U':
                current_bunch = ['bband_flag', 'macd_lite_flag', 'engulfing_flag', 'U']
            if trende_sign == 'D':
                current_bunch = ['bband_flag', 'macd_lite_flag', 'engulfing_flag', 'D']
                
            if trende_sign == 'F':
                if bunch_variant == 2:
                    current_bunch = ['macd_lite_flag', 'stoch_flag', 'F']

            buy_signal, sell_signal = self.bunch_handler_func(next_data, close_price, current_bunch)

            if buy_signal:
                return 1
            elif sell_signal:
                return 2
            else:
                return "neutral"
            
    def get_udf_strategy_signals(self, top_coins, interval):
        pass

get_orders_stek_2 = IND_STR_TWO()
