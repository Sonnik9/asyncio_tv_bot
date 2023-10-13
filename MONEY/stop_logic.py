from pparamss import my_params
from API.create_order import create_orders_obj
from UTILS.calc_qnt import calc_qnt_func

class SL_STRATEGYY():
    def __init__(self) -> None:
        self.t_p = None
        self.s_l = None
        self.sl_atr_multiplier = 1.2 #2.0 
        self.tp_art_multipler = 0.07 

    def sl_controller(self, main_stake):
        # profit = None  
        profit_flag = False  
        print(f"len_main_stake  {len(main_stake)}")    

        for item in main_stake:
            profit = None  
            open_order = None   
            close_order = None  
            qnt = None
        
            try:
                enter_price = item['enter_price']
                if enter_price < 1.1:
                    main_stake.remove(item)
                    break
                current_price = item['current_price']
                symbol = item["symbol"]
                defender = item['defender'] 
                atr = item['atr']
                qnt, _= calc_qnt_func(symbol, enter_price, my_params.DEPO)   
                item['qnt'] = qnt       
                target_point_level = item["target_point_level"]
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str36:___{ex}")      
                continue

            if item['in_position'] == False:
                try:
                    if qnt:
                        is_closing = 1
                        open_order = create_orders_obj.make_order(item, qnt, is_closing)
                        print(open_order)
                        enter_price = open_order['price']
                        # print(open_order)
                except Exception as ex:           
                    print(f"MONEY/stop_logic_1.py_str41:___{ex}")
                if not open_order:
                    main_stake.remove(item)
                    break
                else:
                    item['in_position'] = True

            if item['in_position'] == True:
                if my_params.SL_STRATEGY_NUMBER == 2:
                    profit, target_point_level = self.sl_strategy_two(defender, enter_price, current_price, atr, qnt, target_point_level)
                    item['profit'] = profit
                    
                    if profit: 
                        try:
                            is_closing = -1
                            qnt = item['qnt']
                            close_order = create_orders_obj.make_order(item, qnt, is_closing)
                            if close_order:
                                item["target_point_level"] = target_point_level
                                item['close_order'] = True  
                                profit_flag = True  
                            else:
                                item['profit'] = None

                        except Exception as ex:                         
                            print(f"MONEY/stop_logic_1.py_str56:___{ex}")              
                        break

        return main_stake, profit_flag  

    def calculate_profit_part(self, defender, enter_price, current_price, atr, target_point_level):
        profit_flag = False
        target_point = None
        print(f"target_point_level  {target_point_level}")
        print(defender, enter_price, current_price, atr)

        if defender == 1:
            target_point = enter_price + (target_point_level * atr*self.tp_art_multipler)
            print(f"target_poin_{target_point}")
            dinamic_sl = enter_price + ((target_point - enter_price)/2)
            
            if current_price >= target_point:
                target_point_level += 1
                if target_point_level == 3:                
                    profit_flag = True
            if (target_point_level == 2) and (current_price < target_point) and (current_price >= dinamic_sl):
                profit_flag = True

        elif defender == -1:
            target_point = enter_price - (target_point_level * atr*self.tp_art_multipler)
            print(f"target_poin_{target_point}")
            dinamic_sl = enter_price - ((enter_price - target_point)/2)        

            if current_price <= target_point:                               
                target_point_level += 1
                if target_point_level == 3:                                      
                    profit_flag = True

            if (target_point_level == 2) and (current_price > target_point) and (current_price <= dinamic_sl):
                profit_flag = True

        return profit_flag, target_point_level

    def sl_strategy_two(self, defender, enter_price, current_price, atr, qnt, target_point_level):
        profit = None
        static_sl, profit_flag = None, False
        
        # print(defender, enter_price, current_price, atr, qnt)

        profit_flag, target_point_level = self.calculate_profit_part(defender, enter_price, current_price, atr, target_point_level)

        if defender == 1:
            static_sl = enter_price - atr * self.sl_atr_multiplier
            if (current_price <= static_sl) or profit_flag:
                profit = (current_price - enter_price) * qnt
                return profit, target_point_level
        elif defender == -1:
            static_sl = enter_price + atr * self.sl_atr_multiplier
            if (current_price >= static_sl) or profit_flag:
                profit = (enter_price - current_price) * qnt
                return profit, target_point_level

        return profit, target_point_level


sl_strategies = SL_STRATEGYY(my_params.SL_STRATEGY_NUMBER, my_params.DEPO)
