from pparamss import my_params
from API.create_order import create_orders_obj

class SL_STRATEGYY():
    def __init__(self, sl_strategy_number, depo) -> None:
        self.sl_strategy_number = sl_strategy_number 
        self.depo = depo
        self.t_p = None
        self.s_l = None
        self.atr_multiplier = 1.2 #2.0  

    def sl_controller(self, main_stake):
        # profit = None        
        # qnt = None
        profit_flag = False

        for item1 in main_stake:
            if not item1['in_position']:
                # open_order func
                item1['in_position'] = True
        
        for item in main_stake:
            profit = None            
            # profit, symbol, defender, enter_price, current_price, 
                        
            try:
                # symbol = item["symbol"]
                defender = item['defender']         
                enter_price = item['enter_price']
                current_price = item['current_price']
                atr = item['atr']
                # qnt = item['qnt']  
                qnt = round((my_params.depo / enter_price), 7)           
                range_counter = item["range_counter"]
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str36:___{ex}")
            

            try:
                create_orders_obj.open_order(item, qnt)
            except Exception as ex:
                del item 
                print(f"MONEY/stop_logic_1.py_str41:___{ex}")

            if self.sl_strategy_number == 2:
                profit, range_counter = self.sl_strategy_two(defender, enter_price, current_price, atr, qnt, range_counter)
                item['profit'] = profit
                item["range_counter"] = range_counter
                if profit:
                    item['close_order'] = True  
                    profit_flag = True   
                    try:
                        create_orders_obj.close_order(item, qnt)
                    except Exception as ex:                         
                        print(f"MONEY/stop_logic_1.py_str56:___{ex}")              
                    break

        return main_stake, profit_flag  

    def calculate_profit_part(self, defender, enter_price, current_price, atr, range_counter):
        profit_flag = False
        # print(defender, enter_price, current_price, atr)

        if defender == 1:
            target_point = enter_price * (1 + (range_counter * (atr/15)))
            dinamic_sl = enter_price + ((target_point - enter_price)/2)
            
            if current_price >= target_point:                
                range_counter += 1
                if range_counter == 3:                
                    profit_flag = True
            if (range_counter == 2) and (current_price < target_point) and (current_price >= dinamic_sl):
                profit_flag = True

        elif defender == -1:
            target_point = enter_price * (1 - (range_counter * (atr/15)))
            dinamic_sl = enter_price - ((enter_price - target_point)/2)        

            if current_price <= target_point:                
                range_counter += 1
                if range_counter == 3:                                      
                    profit_flag = True

            if (range_counter == 2) and (current_price > target_point) and (current_price <= dinamic_sl):
                profit_flag = True

        return profit_flag, range_counter

    def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt, range_counter):
        profit = None
        static_sl, profit_flag = None, False
        
        # print(defender, enter_price, current_price, atr, qnt)

        profit_flag, range_counter = self.calculate_profit_part(defender, enter_price, current_price, atr, range_counter)

        if defender == 1:
            static_sl = enter_price - atr * self.atr_multiplier
            if (current_price <= static_sl) or profit_flag:
                profit = (current_price - enter_price) * qnt
                return profit, range_counter
        elif defender == -1:
            static_sl = enter_price + atr * self.atr_multiplier
            if (current_price >= static_sl) or profit_flag:
                profit = (enter_price - current_price) * qnt
                return profit, range_counter

        return profit, range_counter


sl_strategies = SL_STRATEGYY(my_params.sl_strategy_number, my_params.depo)
